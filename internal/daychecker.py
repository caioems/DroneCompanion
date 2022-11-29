import os
import pandas as pd
import simplekml

from pathlib import Path
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

#class containing functions for the data extraction/modeling and kml customization 
class DayChecker:
      
    def create_csv(self, log_path):
        self.types = ["CAM", "EV", "BAT", "MSG", "RCOU", "TERR", "VIBE"]
        log = log_path.as_posix()
        path = log_path.parent
        
        def mycmd(type):
            os.system(f"mavlogdump.py --planner --format csv --types {type} {str(log)} > {str(path)}/{type}.csv")
        
        with ThreadPoolExecutor() as executor:    #max_workers=len(self.types)        
            executor.map(mycmd, self.types)
    
    def create_df(self, log_path, csv_name):
        csv_file = os.path.join(log_path.parent, csv_name + ".csv")
        with Lock():
            with open(csv_file, "r") as csv:
                df = pd.read_csv(csv, engine='c', on_bad_lines = 'skip', index_col='timestamp')
                df.index = pd.to_datetime(df.index, unit='s', origin='unix')
        return df
    
    def create_df_dict(self, flight_log):
        self.df_dict = {}
        for i in self.types:
            self.df_dict[i] = self.create_df(flight_log, i)            
        return self.df_dict 
    
    def delete_csv(self, log_path):
        for t in self.types:
            csv_file = os.path.join(log_path.parent, f'{t}.csv')
            os.remove(csv_file)
    
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
        for index, row in self.df_dict['CAM'].iterrows():
            coords_list.append((row.Lng, row.Lat))
        ls.coords = coords_list
        return ls
    
    def create_balloon_report(self, feature):
        flight_data = self.df_dict['EV'].index[0]
        flight_time = self.df_dict['EV'].index[-1] - flight_data
        base_path = Path(__file__).parent
        template_path = (base_path / "../internal/motororder-quad-x-2d.png").resolve()
        
        #TODO: convert html to file instead of raw coding
        #TODO: balloon being displayed as default          
        feature.balloonstyle.text = f"""<html>
                                        <table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:270px; width:400px">
                                            <tbody>
                                                <tr>
                                                    <td>
                                                    <table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:100%; margin-left:auto; margin-right:auto; opacity:0.95; width:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%">
                                                                <p><span style="font-family:Tahoma,Geneva,sans-serif">Flight time:</span></p>

                                                                <p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{str(flight_time.components.minutes)}m {str(flight_time.components.seconds)}s</span></strong></span></p>
                                                                </td>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%">
                                                                <p><span style="font-family:Tahoma,Geneva,sans-serif">Batt. cons.:</span></p>

                                                                <p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{str(round(self.df_dict['BAT'].CurrTot[-1]))} mAh</span></strong></span></p>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif">Motors status:</span></td>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%">
                                                                <p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.motors_status}</span></strong></span></p>

                                                                <p><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.motors_feedback}&nbsp;</span></p>
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif">IMU Status:</span></td>
                                                                <td style="height:90px; text-align:center; vertical-align:middle; width:50%">
                                                                <p><span style="font-size:20px"><strong><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.imu_status}</span></strong></span></p>

                                                                <p><span style="font-family:Tahoma,Geneva,sans-serif">{self.report.imu_feedback}</span></p>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                    <p>&nbsp;</p>
                                                    </td>
                                                    <td>
                                                    <table align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; height:100%; margin-left:auto; margin-right:auto; width:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif"><span style="color:#2ecc71"><strong><span style="font-size:16px">{self.report.motors_pwm_list[2]}</span></strong></span></span></td>
                                                                <td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif"><strong><span style="font-size:16px"><span style="color:#3498db">{self.report.motors_pwm_list[0]}</span></span></strong></span></td>
                                                            </tr>
                                                            <tr>
                                                                <td colspan="2" style="text-align:center; vertical-align:middle"><span style="font-family:Tahoma,Geneva,sans-serif"><img alt="" src="{template_path.as_uri()}" style="border-style:solid; border-width:0px; height:159px; width:120px" /></span></td>
                                                            </tr>
                                                            <tr>
                                                                <td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif"><span style="font-size:16px"><strong><span style="color:#3498db">{self.report.motors_pwm_list[1]}</span></strong></span></span></td>
                                                                <td style="height:55px; text-align:center; vertical-align:middle; width:50%"><span style="font-family:Tahoma,Geneva,sans-serif"><span style="color:#2ecc71"><span style="font-size:16px"><strong>{self.report.motors_pwm_list[3]}</strong></span></span></span></td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                    <p>&nbsp;</p>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        </html>"""
