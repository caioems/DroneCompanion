import os
import re
import random
import exifread
import simplekml
import numpy as np
import pandas as pd
import internal.config as cfg
import tests.gps_test as gps_test
from internal.concave_hull import concaveHull
from tests.healthtests import HealthTests
from concurrent.futures import ThreadPoolExecutor
from internal.report_temp import balloon_report_template

# Class containing functions for the data extraction/modeling and kml customization
class DayChecker:

    def __init__(self, flight_log):
        """
        Initialize the instance and run the program. This is the entry point for the class.

        @param flight_log - path to a BIN log file
        """
        self.flight_log = flight_log
        self.run()
        
    def __repr__(self):
        return "\n".join([
            f'Flight date: {self.df_dict["EV"].index[0]}',
            f'Flight log: {self.flight_log}'
            ])

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
            internal_dir = os.path.dirname(__file__)
            mavlogdump_path = os.path.join(internal_dir, "mavlogdump.py")
            #mavlogdump_path = "internal\\mavlogdump.py"
            
            os.system(
                f"{mavlogdump_path} --planner --format csv --types {msg_type} {str(log)} > {str(path)}/{msg_type}.csv"
            )

        with ThreadPoolExecutor() as executor:
            executor.map(mycmd, cfg.MESSAGES)

    def create_df(self, csv_name):
        """
        Create a pandas dataframe from a csv file. This is used to create dataframes containing messages that are stored in flight logs.

        @param csv_name - String representing the name of the csv file

        @return pd.DataFrame with index as the column timestamp
        """
        csv_file = os.path.join(self.flight_log.parent, csv_name + ".csv")

        with open(csv_file, "r") as csv:
            df = pd.read_csv(
                csv, 
                on_bad_lines="skip", 
                index_col="timestamp"
                )
            df.index = pd.to_datetime(df.index, unit="s", origin="unix")
        return df

    def create_df_dict(self):
        """
        Create and return a dictionary of dataframes. Keys are each of cfg.MESSAGES and values are their respective pandas DataFrames.


        @return Dictionary of dataframes
        """
        self.df_dict = {i: self.create_df(i) for i in cfg.MESSAGES}
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
            executor.map(delete_all_csv, cfg.MESSAGES)

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
            if cfg.CAMERA_ISO_RANGE[0] <= mdata["EXIF ISOSpeedRatings"].values[0] <= cfg.CAMERA_ISO_RANGE[1]:
                self.mdata_test["ISO"] = ["OK"]
            else:
                self.mdata_test["ISO"] = ["FAIL", "Check camera ISO."]

            # Camera's shutter speed
            if str(mdata["EXIF ExposureTime"]) == cfg.CAMERA_SHUTTER:
                self.mdata_test["Shutter"] = ["OK"]
            else:
                self.mdata_test["Shutter"] = ["FAIL", "Check camera shutter speed."]

            # Camera's copyright
            if re.match(cfg.CAMERA_COPYRIGHT_PATTERN, mdata["Thumbnail Copyright"].values):
                self.mdata_test["Copyright"] = ["OK"]
            else:
                self.mdata_test["Copyright"] = ["FAIL", "Check camera copyright."]

            # Camera's artist
            if re.match(cfg.CAMERA_ARTIST_PATTERN, mdata["Image Artist"].values):
                self.mdata_test["Artist"] = ["OK"]
            else:
                self.mdata_test["Artist"] = ["FAIL", "Check camera artist."]

            keys = self.mdata_test.keys()
            # This method will set the result of the sensor test.
            if all(self.mdata_test[test][0] == "OK" for test in keys):
                self.mdata_test["Result"] = ["OK", "No sensor issues"]
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
        seqlog = [f for f in os.listdir(path) if f.startswith(cfg.RAW_GNSS_LOG_NAME)]
        self.seqlog_test = {}
        
        if seqlog:
            seqlog_rtcm = os.path.join(
                path, 
                f"{cfg.RAW_GNSS_LOG_NAME}.txt"
                )
            seqlog_rinex = os.path.join(
                path, 
                f"{cfg.RAW_GNSS_LOG_NAME}.obs"
                )

            gps_test.parse_rtcm_to_rinex(seqlog_rtcm)
            rinex_epochs = gps_test.get_rinex_epochs(seqlog_rinex)

            self.seqlog_test['gps_freq'] = gps_test.check_gps_frequency(rinex_epochs)

            self.seqlog_test['gps_date'] = gps_test.check_gps_date(rinex_epochs)
            
            keys = self.seqlog_test.keys()
            if all(self.seqlog_test[test][0] == 'OK' for test in keys):
                self.seqlog_test['Result'] = ('OK', 'No issues related to GPS')        
            else:
                for test in keys:
                    if self.seqlog_test[test][0] != 'OK':
                        error_found = True
                        error_message = self.seqlog_test[test]
                        
                if error_found:
                    self.seqlog_test['Result'] = error_message
        else:
            self.seqlog_test['Result'] = ('WARN', 'No SEQLOG found')
    
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
            (row.Lng, row.Lat) for _, row in self.df_dict["CAM"].iterrows()
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
        Set the style of the simplekml.LineString based on the results of the tests.
         
         @param feature - linestring to be stylized
        """
        new_style = simplekml.Style(
            linestyle=simplekml.LineStyle(
                width=cfg.LINESTYLE_WIDTH, 
                color=cfg.LINESTYLE_COLOR
                )
            )

        if 'FAIL' in (
            self.mdata_test["Result"][0],
            self.seqlog_test["Result"][0], 
            self.htests.trig_status, 
            self.htests.vcc_status, 
            self.htests.motors_status):
            
            new_style.linestyle.color = simplekml.Color.yellow            

        feature.style = new_style
            
    def get_drone_uid(self):
        """Gets the flight controller serial number.

        Returns:
            str: Flight controller number
        """
        msgs = self.df_dict["MSG"]
        mask = msgs["Message"].str.startswith('Pixhawk')
        raw_uid = msgs[mask]['Message'].iloc[0].split()
        return ''.join(raw_uid[1:])
    
    def get_drone_no(self):
        """Gets the drone internal ID based on a module containing the serial dict. If didn't find it, it returns the full UID number.

        Returns:
            str: Flight controller internal ID
        """
        from internal.drones import serial_dict
        
        return serial_dict.get(self.drone_uid, self.drone_uid)

    def create_balloon_report(self, feature):
        """
         Create a report for the linestrings and save it to the KML file. It is used to show a balloon with useful information in google earth.
         
         @param feature - linestring to be stylized
        """
        flight_date = self.df_dict["EV"].index[0]
        flight_time = self.df_dict["EV"].index[-1] - flight_date
                
        #Text variables
        drone_no = self.get_drone_no()
        f_time = f"{flight_time.components.minutes}m {flight_time.components.seconds}s"
        batt_cons = f"{str(round(self.df_dict['BAT'].CurrTot.iloc[-1]))} mAh"
        photos = f"{self.mdata_test['Result'][0]}"
        photos_fb = f"{self.mdata_test['Result'][1]}"
        trigger = f"{self.htests.trig_status}"
        trig_fb = f"{self.htests.trig_feedback}"
        motors = f"{self.htests.motors_status}"
        motors_fb = f"{self.htests.motors_feedback}"
        imu = f"{self.htests.imu_status}"
        imu_fb = f"{self.htests.imu_feedback}"
        vcc = f"{self.htests.vcc_status}"
        vcc_fb = f"{self.htests.vcc_feedback}"
        gps = f"{self.seqlog_test['Result'][0]}"
        gps_fb = f"{self.seqlog_test['Result'][1]}"

        feature.balloonstyle.text = balloon_report_template(
            drone_no,
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
            vcc,
            vcc_fb,
            gps,
            gps_fb
            )
        
    def run(self):
        """
        This is the main method of the class. It will create the CSV files, the dataframes from the data files, and then delete the CSV files. It also runs the metadata tests and create the health reports.
        """
        try:
            self.create_csv()
            self.create_df_dict()
            self.delete_csv()
            self.metadata_test()
            self.seqlog_check()

            self.flight_timestamp = str(self.df_dict["EV"].index[0].timestamp())
            self.drone_uid = self.get_drone_uid()
            
            # Running the drone health tests
            self.htests = HealthTests(
                self.df_dict["RCOU"],
                self.df_dict["VIBE"],
                self.df_dict["POWR"],
                self.df_dict["CAM"],
                self.df_dict["TRIG"],
            )
            self.htests.run()
            
        except Exception as e:
            print(f'Failed! Error: {e}')
