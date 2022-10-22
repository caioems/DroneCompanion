import os
import pandas as pd
import simplekml    


class DayChecker:    
    def create_csv(self, log_path):
        types = ["CAM", "EV", "BAT", "RCOU", "VIBE"]
        log = log_path.as_posix()
        path = log_path.parent
        for t in types:    
            mycmd = "mavlogdump.py --planner --format csv --types " + t + " " + str(log) + " > " + str(path) + "/" + t + ".csv"
            os.system(mycmd)
    
    def create_df(self, log_path, csv_name):
        global file, csv_file
        file = csv_name + ".csv"
        csv_file = os.path.join(log_path.parent, file)
        df = pd.read_csv(csv_file, index_col='timestamp')
        df.index = pd.to_datetime(df.index, unit='s', origin='unix')
        os.remove(csv_file)
        return df
    
    #creating kml containers
    
    def rgb_style(self, feature):
        rgb_style = simplekml.Style()
        rgb_style.linestyle.color = simplekml.Color.whitesmoke
        rgb_style.linestyle.width = 2.0
        feature.style = rgb_style
        
    def agr_style(self, feature):
        agr_style = simplekml.Style()
        agr_style.linestyle.color = simplekml.Color.red
        agr_style.linestyle.width = 2.0
        feature.style = agr_style
    
    def create_linestring(self, log_path, kml, container_index):
        ls = kml.containers[container_index].newlinestring(name = log_path.name)
        coords_list = []
        for index, row in self.cam_df.iterrows():
            coords_list.append((row.Lng, row.Lat))
        ls.coords = coords_list
        return ls
    
    def create_balloon_report(self, feature):
        flight_time = self.ev_df.index[-1] - self.ev_df.index[0]  
        feature.balloonstyle.text = "Flight time: " + str(flight_time.components.minutes) + "m " + str(flight_time.components.seconds) + "s \n" +\
                                    "Bat. consumed: " + str(round(self.bat_df.CurrTot[-1])) + " mAh \n" +\
                                    "\n" +\
                                    "Motors: " + self.report.motors_status + self.report.motors_feedback + "\n" +\
                                    "Vibration: " + self.report.imu_status + self.report.imu_feedback #"\n" +\
                                    #"EKF variance: " + errors.ekf_count() + "\n" +\
                                    #"GPS glitch: " + errors.gps_glitch_count() 