import pandas as pd
from statistics import mean

class HealthTests:
    def __init__(self, rcou_df, vibe_df):
        self.__rcou_df = rcou_df
        self.__vibe_df = vibe_df 
        self.motors_status = 'UNKNOWN'
        self.motors_feedback = ''
        self.imu_status = 'UNKNOWN'
        self.imu_feedback = ''
        self.gps_status = 'UNKNOWN'
        self.gps_feedback = ''
        
    def motor_test(self):
        self.motors_status = 'OK - '
        self.motors_feedback = 'balanced'
        
        pwm_df = pd.DataFrame({'1':[mean(self.__rcou_df.C1), max(self.__rcou_df.C1)],
                               '2':[mean(self.__rcou_df.C2), max(self.__rcou_df.C2)], 
                               '3':[mean(self.__rcou_df.C3), max(self.__rcou_df.C3)],
                               '4':[mean(self.__rcou_df.C4), max(self.__rcou_df.C4)]}).T
        pwm_df.columns = ["mean", "max"]        
        day_avg = str(int(mean(pwm_df["mean"])))
        avg_list = str([int(x) for x in pwm_df["mean"]])
        max_min = str(int(max(pwm_df["mean"]) - min(pwm_df["mean"])))              
        
        if int(max_min) > 75:
            self.motors_status = 'WARN - '
            self.motors_feedback = 'avg motors pwm: ' + day_avg + " " + avg_list + '. Difference between min and max motor averages: ' + max_min
        elif int(max_min) > 150:
            self.motors_status = 'FAIL - '
            self.motors_feedback = 'avg motors pwm: ' + day_avg + " " + avg_list + '. Difference between min and max motor averages: ' + max_min
            
            
    def vibe_test(self):
        self.imu_status = 'OK - '
        self.imu_feedback = 'no vibe issues'
        
        clips = (self.__vibe_df.Clip0[-1], self.__vibe_df.Clip1[-1], self.__vibe_df.Clip2[-1])
        vibes = (mean(self.__vibe_df.VibeX), mean(self.__vibe_df.VibeY), mean(self.__vibe_df.VibeZ))
        
        if any(v > 30 for v in vibes):
            max_vibes = str(round(max(vibes), 1))
            self.imu_status = 'WARN - '
            self.imu_feedback = 'several vibration (' + max_vibes + ' m/s/s)'
        elif any(c > 0 for c in clips):
            max_clips = str(max(clips))
            self.imu_status = 'FAIL - '
            self.imu_feedback = 'accel was clipped ' + max_clips + ' times'
    
    def run(self):
        self.motor_test()
        self.vibe_test()    