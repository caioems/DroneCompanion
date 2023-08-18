import os
import re
import random
import exifread
import simplekml
import numpy as np
import pandas as pd
import tests.gps_test as gps_test
from pathlib import Path
from internal.concave_hull import concaveHull
from tests.healthtests import HealthTests
from concurrent.futures import ThreadPoolExecutor
from internal.report_temp import balloon_report_template


# class containing functions for the data extraction/modeling and kml customization
class DayChecker:
    messages = ["CAM", "EV", "BAT", "MSG", "POWR", "RCOU", "VIBE", "TRIG"]

    def __init__(self, flight_log):
        """
        Initialize the instance and run the program. This is the entry point for the class.

        @param flight_log - path to a BIN log file
        """
        self.flight_log = flight_log
        self.run()

    def create_csv(self):
        """
        Create csv files from a list of messages within a flight log. It uses a thread pool to take advantage of asynchronous execution.
        
        """
        log = self.flight_log.as_posix()
        path = self.flight_log.parent

        def mycmd(msg_type):
            """
            Dump specific messages from log to file. This is a wrapper around mavlogdump.py

            @param msg_type - String representing the message type (ex.: "CAM")
            """
            os.system(
                f"mavlogdump.py --planner --format csv --types {msg_type} {str(log)} > {str(path)}/{msg_type}.csv"
            )

        with ThreadPoolExecutor() as executor:
            executor.map(mycmd, DayChecker.messages)

    def create_df(self, csv_name):
        """
        Create a pandas dataframe from a csv file. This is used to create dataframes containing messages that are stored in flight logs.

        @param csv_name - String representing the name of the csv file

        @return pd.DataFrame with index as the column timestamp
        """
        csv_file = os.path.join(self.flight_log.parent, csv_name + ".csv")

        with open(csv_file, "r") as csv:
            df = pd.read_csv(csv, on_bad_lines="skip", index_col="timestamp")
            df.index = pd.to_datetime(df.index, unit="s", origin="unix")
        return df

    def create_df_dict(self):
        """
        Create and return a dictionary of dataframes. Keys are each of DayChecker.messages and values are their respective pandas DataFrames.


        @return Dictionary of dataframes
        """
        self.df_dict = {i: self.create_df(i) for i in DayChecker.messages}
        return self.df_dict

    def delete_csv(self):
        """
        Delete all CSV files in a thread pool to take advantage of asynchronous execution.
        """

        def delete_all_csv(msg_type):
            """
            Delete all csv files of a given message type.
            
            @param msg_type - String representing the message type (ex.: "CAM")
            """
            csv_file = os.path.join(self.flight_log.parent, f"{msg_type}.csv")
            os.remove(csv_file)

        with ThreadPoolExecutor() as executor:
            executor.map(delete_all_csv, DayChecker.messages)

    def metadata_test(self):
        """
        Gets the metadata of random JPG files and run tests on it to make sure the JPG contains specific parameters.

        """
        self.mdata_test = {}
        img_path = self.flight_log.parent

        def get_random_image_metadata():
            """
            Get metadata for a random image. This is useful for getting the EXIF data from an image taken as a sample of a bigger batch of images.


            @return A dictionary of exif data for the image.
            """
            files = [f for f in os.listdir(img_path) if f.endswith(".JPG")]
            random_file = random.choice(files)
            with open(os.path.join(img_path, random_file), "rb") as f:
                exif_data = exifread.process_file(f)
            return exif_data

        try:
            mdata = get_random_image_metadata()

            # Camera's ISO
            if 100 <= mdata["EXIF ISOSpeedRatings"].values[0] <= 1600:
                self.mdata_test["ISO"] = ["OK"]
            else:
                self.mdata_test["ISO"] = ["FAIL", "Check camera ISO."]

            # Camera's shutter speed
            if str(mdata["EXIF ExposureTime"]) == "1/1600":
                self.mdata_test["Shutter"] = ["OK"]
            else:
                self.mdata_test["Shutter"] = ["FAIL", "Check camera shutter speed."]

            # Camera's copyright
            if re.match(r"a[0-9]r[0-9]_[a-z]{3}", mdata["Thumbnail Copyright"].values):
                self.mdata_test["Copyright"] = ["OK"]
            else:
                self.mdata_test["Copyright"] = ["FAIL", "Check camera copyright."]

            # Camera's artist
            if re.match(r"^\d{7}$", mdata["Image Artist"].values):
                self.mdata_test["Artist"] = ["OK"]
            else:
                self.mdata_test["Artist"] = ["FAIL", "Check camera artist."]

            keys = self.mdata_test.keys()
            # This method will set the result of the sensor test.
            if all(self.mdata_test[test][0] == "OK" for test in keys):
                self.mdata_test["Result"] = ["OK", "no sensor issues"]
            else:
                # This method will set the result of all tests in the test dictionary
                for test in keys:
                    # This method is used to test the result of the test.
                    if self.mdata_test[test][0] != "OK":
                        self.mdata_test["Result"] = self.mdata_test[test]
        except Exception as e:
            print(f"Error ocurred in the metadata test: {str(e)}")
    
    def seqlog_check(self):
        path = self.flight_log.parent
        seqlog = [f for f in os.listdir(path) if f.startswith("SEQ")]
        
        if len(seqlog) > 0:
            seqlog_rtcm = os.path.join(path, "SEQLOG00.txt")
            seqlog_rinex = os.path.join(path, "SEQLOG00.obs")
            
            gps_test.convert_rtcm_to_rinex(seqlog_rtcm)
            obs_times = gps_test.get_rinex_times(seqlog_rinex)
            obs_freq = gps_test.check_obs_frequency(obs_times)
            obs_period = gps_test.check_obs_period(obs_times)
            
            self.seqlog_test = (obs_freq, obs_period)
        else:
            self.seqlog_test = (True, True)
    
    def create_linestring(self, kml):
        """Creates a linestring feature based on the lat and lon of the CAM messages within the log.

        Args:
            kml (simplekml.Kml): The Kml object that will hold the
            linestring

        Returns:
            simplekml.LineString: The LineString object
        """

        ls = kml.newlinestring(name=self.flight_log.name)
        coords_list = [
            (row.Lng, row.Lat) for index, row in self.df_dict["CAM"].iterrows()
        ]
        ls.coords = coords_list
        return ls

    #TODO: add condition for merging polygons of merged flights
    def create_polygon(self, kml, container_index):
        """
         **NEEDS FIX**
         Create and return a polygon for the KML. The polygons are created by using the concave hull technique.
         
         @param kml (simplekml.Kml) - The Kml object that will hold the linestring
         @param container_index - The index of the container that will contain the polygon
         
         @return The polygon created in the KML file and added to
        """
        poly = kml.containers[container_index].newpolygon(name=self.flight_log.name)
        coords_list = [
            (row.Lng, row.Lat) for index, row in self.df_dict["CAM"].iterrows()
        ]
        coords_list = np.array(coords_list)
        poly.outerboundaryis = concaveHull(coords_list, 3)
        return poly

    def change_line_style(self, feature):
        """
        Set the style of the simplekml.LineString. It is used to indicate the sensor used in the flight.
         
         @param feature - linestring to be stylized
        """
        new_style = simplekml.Style()
        new_style.linestyle.width = 2.0
        
        if 'FAIL' in self.mdata_test["Result"][0]:
            new_style.linestyle.color = simplekml.Color.yellow        
        elif not (self.seqlog_test[0] & self.seqlog_test[1]):
            new_style.linestyle.color = simplekml.Color.yellow            
        elif 'FAIL' in self.report.trig_status:
            new_style.linestyle.color = simplekml.Color.yellow            
        else:
            new_style.linestyle.color = simplekml.Color.red
        
        #//OLD LOGIC//
        # if "OK" in self.mdata_test["Result"][0]:
        #     new_style.linestyle.color = simplekml.Color.red
        # #checking seqlog consistency
        # elif (self.seqlog_test[0] & self.seqlog_test[1]):
        #     new_style.linestyle.color = simplekml.Color.red
        # elif self.report.trig_status == 'OK':
        #     new_style.linestyle.color = simplekml.Color.red
        # else:
        #     new_style.linestyle.color = simplekml.Color.yellow
        
        feature.style = new_style
            
    def get_drone_uid(self):
        msgs = self.df_dict["MSG"]
        mask = msgs["Message"].str.startswith('Pixhawk')
        raw_uid = msgs[mask]['Message'][0].split()
        drone_uid = ''.join(raw_uid[1:])
        return drone_uid

    #TODO: error dealing when BAT sheet is filled with NaN
    def create_balloon_report(self, feature):
        """
         Create a report for the linestrings and save it to the KML file. It is used to show a balloon with useful information in google earth.
         
         @param feature - linestring to be stylized
        """
        flight_date = self.df_dict["EV"].index[0]
        flight_time = self.df_dict["EV"].index[-1] - flight_date
                
        #Text variables
        drone_uid = self.drone_uid
        f_time = f"{str(flight_time.components.minutes)}m {str(flight_time.components.seconds)}s"
        batt_cons = f"{str(round(self.df_dict['BAT'].CurrTot[-1]))} mAh"
        photos = f"{self.mdata_test['Result'][0]}"
        photos_fb = f"{self.mdata_test['Result'][1]}"
        trigger = f"{self.report.trig_status}"
        trig_fb = f"{self.report.trig_feedback}"
        motors = f"{self.report.motors_status}"
        motors_fb = f"{self.report.motors_feedback}"
        imu = f"{self.report.imu_status}"
        imu_fb = f"{self.report.imu_feedback}"
        vcc = f"{self.report.vcc_status}"
        vcc_fb = f"{self.report.vcc_feedback}"
        gps_freq = f"{'Frequency OK (5 Hz)' if self.seqlog_test[0] == True else 'Bad observations frequency'}"
        gps_period = f"{'period OK (same day)' if self.seqlog_test[1] == True else 'bad period (at least two days in the SEQLOG file)'}"

        feature.balloonstyle.text = balloon_report_template(
            #TODO: add drone uid to template
            drone_uid,
            flight_date,
            f_time, 
            batt_cons, 
            photos, 
            photos_fb,
            motors,
            motors_fb,
            trigger,
            trig_fb,
            imu,
            imu_fb,
            gps_freq,
            gps_period,
            vcc,
            vcc_fb
            )
        
    def run(self):
        """
        This is the main method of the class. It will create the CSV files, the dataframes from the data files, and then delete the CSV files. It also runs the metadata tests and create the health reports.
        """
        self.create_csv()
        self.create_df_dict()
        self.delete_csv()
        self.metadata_test()
        self.seqlog_check()

        self.flight_timestamp = str(self.df_dict["EV"].index[0].timestamp())
        self.drone_uid = self.get_drone_uid()
        
        # Running the drone health tests
        self.report = HealthTests(
            self.df_dict["RCOU"],
            self.df_dict["VIBE"],
            self.df_dict["POWR"],
            self.df_dict["CAM"],
            self.df_dict["TRIG"],
        )
        self.report.run()
