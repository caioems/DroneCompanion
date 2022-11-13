import pandas as pd
from statistics import mean

class HealthTests:
    def __init__(self, rcou_df, vibe_df):
        self._rcou_df = rcou_df
        self._vibe_df = vibe_df 
        self.motors_status = 'UNKNOWN'
        self.motors_feedback = ''
        self.imu_status = 'UNKNOWN'
        self.imu_feedback = ''
        self.gps_status = 'UNKNOWN'
        self.gps_feedback = ''
        
    def __repr__(self):
        return (
            f"motors_status = {self.motors_status}\n"
            f"motors_feedback = {self.motors_feedback}\n"
            f"imu_status = {self.imu_status}\n"
            f"imu_feedback = {self.imu_feedback}\n"
            f"gps_status = {self.gps_status}\n"
            f"gps_feedback = {self.gps_feedback}"
            )
        
        
    def motor_test(self):
        self.motors_status = 'OK'
        self.motors_feedback = 'balanced'
        self.motors_pwm_list = []
        
        pwm_df = pd.DataFrame(
            {
                '1':[mean(self._rcou_df.C1), max(self._rcou_df.C1)],
                '2':[mean(self._rcou_df.C2), max(self._rcou_df.C2)], 
                '3':[mean(self._rcou_df.C3), max(self._rcou_df.C3)],
                '4':[mean(self._rcou_df.C4), max(self._rcou_df.C4)]
            }
        ).T
        pwm_df.columns = ["mean", "max"]
                
        day_avg = str(int(mean(pwm_df["mean"])))
        self.motors_pwm_list = [int(x) for x in pwm_df["mean"]]
        avg_list = str(self.motors_pwm_list)
        # max_min = str(int(max(pwm_df["mean"]) - min(pwm_df["mean"])))              
        
        # if int(max_min) > 75:
        #     self.motors_status = 'WARN'
        #     self.motors_feedback = f'avg motors pwm: {day_avg} {avg_list}. Difference between min and max motor averages: {max_min}.'
        # elif int(max_min) > 150:
        #     self.motors_status = 'FAIL'
        #     self.motors_feedback = f'avg motors pwm: {day_avg} {avg_list}. Difference between min and max motor averages: {max_min}.'
        
        fmotors = abs(self.motors_pwm_list[0] - self.motors_pwm_list[2])
        bmotors = abs(self.motors_pwm_list[1] - self.motors_pwm_list[3])
        warn_level = 30
        fail_level = 45
        
        if fmotors >= warn_level or bmotors >= warn_level:
            if fmotors >= warn_level:
                bad_pwm = max([self.motors_pwm_list[0], self.motors_pwm_list[2]])
                bad_motor = str(self.motors_pwm_list.index(bad_pwm)+1)
                self.motors_status = 'WARN'
                self.motors_feedback = f'Small difference between frontal motors PWM. Check motor {bad_motor}.'
            
            elif bmotors >= warn_level:
                bad_pwm = max([self.motors_pwm_list[1], self.motors_pwm_list[3]])
                bad_motor = str(self.motors_pwm_list.index(bad_pwm)+1)
                self.motors_status = 'WARN'
                self.motors_feedback = f'Small difference between back motors PWM. Check motor {bad_motor}.'
                
            elif fmotors >= fail_level or bmotors >= fail_level:
                if fmotors >= fail_level:
                    bad_pwm = max([self.motors_pwm_list[0], self.motors_pwm_list[2]])
                    bad_motor = str(self.motors_pwm_list.index(bad_pwm)+1)
                    self.motors_status = 'FAIL'
                    self.motors_feedback = f'Big difference in frontal motors PWM\'s avg. Check motor {bad_motor}.'
            
                elif bmotors >= fail_level:
                    bad_pwm = max([self.motors_pwm_list[1], self.motors_pwm_list[3]])
                    bad_motor = str(self.motors_pwm_list.index(bad_pwm)+1)
                    self.motors_status = 'FAIL'
                    self.motors_feedback = f'Big difference in frontal motors PWM\'s avg. Check motor {bad_motor}.'        
                
                
            
    def vibe_test(self):
        self.imu_status = 'OK'
        self.imu_feedback = 'no vibe issues'
        
        clips = (self._vibe_df.Clip0[-1], self._vibe_df.Clip1[-1], self._vibe_df.Clip2[-1])
        vibes = (mean(self._vibe_df.VibeX), mean(self._vibe_df.VibeY), mean(self._vibe_df.VibeZ))
        
        if any(v > 30 for v in vibes):
            max_vibes = str(round(max(vibes), 1))
            self.imu_status = 'WARN'
            self.imu_feedback = f'several vibration ({max_vibes} m/s/s).'
        elif any(c > 0 for c in clips):
            max_clips = str(max(clips))
            self.imu_status = 'FAIL'
            self.imu_feedback = f'accel was clipped {max_clips} times.'
    
    def run(self):
        self.motor_test()
        self.vibe_test()
        return self    