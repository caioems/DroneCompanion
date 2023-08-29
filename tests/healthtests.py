import pandas as pd
from statistics import mean

# TODO: motor efficiency = Thrust (grams) x Power (watts)
class HealthTests:
    def __init__(self, rcou_df, vibe_df, powr_df, cam_df, trig_df):
        """
         Initialize the object. It stores dataframes and apply logical
         tests to point out status and feedback of UAV hardware.
         
         @param rcou_df - dataframe with RCOU data (motors)
         @param vibe_df - dataframe with VIBE data (vibration)
         @param powr_df - dataframe with POWR data (board voltage)
         @param cam_df - dataframe with CAM data (camera messages)
         @param trig_df - dataframe with TRIG data (camera trigger)
        """
        self._rcou_df = rcou_df
        self._vibe_df = vibe_df
        self._powr_df = powr_df
        self._cam_df = cam_df
        self._trig_df = trig_df

        self.motors_status = None
        self.motors_feedback = None
        self.imu_status = None
        self.imu_feedback = None
        self.vcc_status = None
        self.vcc_feedback = None
        self.trig_status = None
        self.trig_feedback = None

    def __repr__(self):
        return f"\n".join([
            f"motors_status = {self.motors_status}",
            f"motors_feedback = {self.motors_feedback}",
            f"imu_status = {self.imu_status}",
            f"imu_feedback = {self.imu_feedback}",
            f"vcc_status = {self.vcc_status}",
            f"vcc_feedback = {self.vcc_feedback}",
            f"trig_status = {self.trig_status}",
            f"trig_feedback = {self.trig_feedback}"
        ])

    def motor_test(self):
        """
         This is a test to see if it's possible to predict 
         motors maintenance. It compares each servo channel 
         output to detect imbalance. Change warn and fail 
         levels as needed.         
        """
        warn_level = 30
        fail_level = 45
        
        self.motors_status = "OK"
        self.motors_feedback = "Motors are balanced"
        self.motors_pwm_list = []

        pwm_df = pd.DataFrame(
            {
                "1": [mean(self._rcou_df.C1), max(self._rcou_df.C1)],
                "2": [mean(self._rcou_df.C2), max(self._rcou_df.C2)],
                "3": [mean(self._rcou_df.C3), max(self._rcou_df.C3)],
                "4": [mean(self._rcou_df.C4), max(self._rcou_df.C4)],
            }
        ).T
        pwm_df.columns = ["mean", "max"]

        self.motors_pwm_list = [int(x) for x in pwm_df["mean"]]

        # Comparing frontal motors and back motors
        fmotors_diff = abs(self.motors_pwm_list[0] - self.motors_pwm_list[2])
        bmotors_diff = abs(self.motors_pwm_list[1] - self.motors_pwm_list[3])
        
        if fmotors_diff >= warn_level or bmotors_diff >= warn_level:
            self.motors_status = "WARN"
            diff_type = "frontal" if fmotors_diff >= warn_level else "back"
            self.motors_feedback = f'Small difference in {diff_type} motors output.'

        if fmotors_diff >= fail_level or bmotors_diff >= fail_level:
            self.motors_status = "FAIL"
            diff_type = "frontal" if fmotors_diff >= fail_level else "back"
            self.motors_feedback = f'Big difference in {diff_type} motors output.'

    def vibe_test(self):
        """
        This is a test to make sure there are no issues related 
        with UAV vibration.
        
        """
        max_vibration = 30 #m/s/s
        
        self.imu_status = "OK"
        self.imu_feedback = "No vibe issues"
        
        vibes = [
            mean(self._vibe_df.VibeX), 
            mean(self._vibe_df.VibeY), 
            mean(self._vibe_df.VibeZ)
            ]
        
        if any(v > max_vibration for v in vibes):
            max_vibes = round(max(vibes), 1)
            self.imu_status = "WARN"
            self.imu_feedback = f"Several vibration ({max_vibes} m/s/s)."
        
        clips = [
            self._vibe_df.Clip0[-1], 
            self._vibe_df.Clip1[-1], 
            self._vibe_df.Clip2[-1]
            ]
        
        if any(c > 0 for c in clips):
            max_clips = max(clips)
            self.imu_status = "FAIL"
            self.imu_feedback = f"Accel was clipped {max_clips} times."
    
    def vcc_test(self):
        """
         This is a test to see if there are voltage issues going on at the 
         flight controller.
         
        """
        self.vcc_mean = round(self._powr_df.Vcc.mean(), 2)
        self.vcc_std = round(self._powr_df.Vcc.std(), 2)

        self.vcc_status = "OK"
        self.vcc_feedback = (
            f"No board voltage issues ({self.vcc_mean}v, ±{self.vcc_std}v)"
        )

        # Check the voltage deviation of the board
        if self.vcc_std >= 0.1:
            self.vcc_status = "WARN"
            self.vcc_feedback = (
                f"Small voltage deviation ({self.vcc_mean}v, ±{self.vcc_std}v)"
            )
        if self.vcc_std >= 0.15:
            self.vcc_status = "FAIL"
            self.vcc_feedback = (
                f"Big voltage deviation ({self.vcc_mean}v, ±{self.vcc_std}v)"
            )
        
        # Check the avg voltage of the board
        if self.vcc_mean < 5:
            self.vcc_status = "WARN"
            self.vcc_feedback = (
                f"Internal board voltage is low ({self.vcc_mean}v, ±{self.vcc_std}v)"
            )   
        if self.vcc_mean < 4.9:
            self.vcc_status = "FAIL"
            self.vcc_feedback = (
                f"Internal board voltage is too low! ({self.vcc_mean}v, ±{self.vcc_std}v)"
            )

    def trig_test(self):
        """
         Test the trigger and camera messages to see if the camera is
         shooting properly.
         
        """
        triggers = self._trig_df.shape[0]
        feedbacks = self._cam_df.shape[0]
        
        if triggers == feedbacks:
            self.trig_status = "OK"
            self.trig_feedback = f"No photos skipped ({triggers})"
        elif triggers > feedbacks:
            self.trig_status = "FAIL"
            self.trig_feedback = (f"{triggers - feedbacks} photos were taken without feedback")
        elif triggers < feedbacks:
            self.trig_status = "FAIL"
            self.trig_feedback = f"There were {feedbacks - triggers} false feedbacks"

    def run(self):
        """
         Run all the tests. This is the main method.
         
         
         @return self
        """
        self.motor_test()
        self.vibe_test()
        self.vcc_test()
        self.trig_test()
        return self
