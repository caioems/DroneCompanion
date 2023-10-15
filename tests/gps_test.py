import os, subprocess
import georinex as gr
import pandas as pd
from pyrtcm import RTCMReader, rtcmhelpers


def parse_rtcm_to_rinex(rtcm_file, method='rtklib'):
    """Takes the path to a RTCM3 binary text file and parses it to a RINEX obs file (using CONVBIN tool from RTKLIB by default).

    :param rtcm_file: File path to RTCM3 file
    :type rtcm_file: str
    :param method: Parsing tool, defaults to 'rtklib'
    :type method: str, optional
    :raises FileNotFoundError: In case of the RTCM3 file is not found
    """
    if not os.path.exists(rtcm_file):
        raise FileNotFoundError(f"RTCM3 file not found: {rtcm_file}")

    # def calculates_hash():
    #     from hashlib import md5
        
    #     hash_obj = md5()
    #     with open(rtcm_file, 'rb') as file:
    #         while True:
    #             data = file.read(65536)
    #             if not data:
    #                 break
    #             hash_obj.update(data)
    #     return hash_obj.hexdigest()

    if method == 'rtklib':
        try:
            command = f"convbin.exe -r rtcm3 -v 3.03 {rtcm_file}"
            return subprocess.run(
                command, 
                 stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, 
                shell=True
                )
        except Exception:
            print(f"RTCM3 file could not be parsed - {Exception}")

    elif method == 'ringo':
        try:
            command = f"ringo.exe rtcmgo {rtcm_file} --outver 3.03 --outobs {rtcm_file[:-3]}obs"
            subprocess.run(
                command, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                shell=True
                )
        except Exception:
            print(f"RTCM3 file could not be parsed - {Exception}")

#TODO: fix this method - use rtcmhelpers.tow2utc() to get the HH:MM:SS.ffffff time related to the beginning of the day then convert it to pd.Timestamp)       
def parse_rtcm_to_dataset(rtcm_file):
    """
    Function to read observation times from an RTCM3 file using RTCMReader.
    :param rtcm_file: Path to the RTCM3 file.
    
    :return: List of observation times.
    """
    if not os.path.exists(rtcm_file):
        raise FileNotFoundError(f"RTCM3 file not found: {rtcm_file}")
    
    def epochs_yield():
        raw_file = open(rtcm_file, 'rb')
        rtcm = RTCMReader(raw_file)
        for _, parsed_data in rtcm:
            try:
                yield parsed_data
            except AttributeError:
                continue
            
    epochs_list = list(epochs_yield())
    return epochs_list
            
def get_rinex_epochs(rinex_file, keep_rinex_file=False):
    """
    Function to get the epochs of a rinex file.
    :param rinex_file: Path to the RINEX obs file.
    :type rinex_file: str
    :type r_epochs: pd.DateTimeIndex
    """
    if not os.path.exists(rinex_file):
        raise FileNotFoundError(f"RINEX file not found: {rinex_file}")

    r_epochs = gr.obstime3(rinex_file)
    r_epochs = pd.to_datetime(r_epochs)
    if not keep_rinex_file:
        os.remove(rinex_file)
    return r_epochs

def check_gps_frequency(rinex_epochs):
    """
    Calculates the time delta of consecutive observations 
    and then checks the median frequency observed.
    
    :param obs_times: pd.DateTimeIndex of the observations
    :return: bool
    """
    timedeltas = rinex_epochs.to_series().diff()
    freq_test = pd.Timedelta(microseconds=199999) <= timedeltas.median()<= pd.Timedelta(microseconds=200001)

    return ('OK', '') if freq_test else ('FAIL', 'Bad GPS frequency')     

def check_gps_date(rinex_epochs, days=1):
    """
    Function that check the period (days) of the observations. If there are
    observations from different days within the log, returns false.
    
    :param obs_times: pd.DateTimeIndex containing the datetime of each observation.
    :param days: int of how many days are tolerable within the log
    """
    recorded_days = rinex_epochs.day
    return ('OK', '') if recorded_days.nunique() == days else ('FAIL', 'Two or more days within SEQLOG')

def check_epochs_ratio(rinex_epochs, min_ratio, gps_freq = 0.2):    
    """
    Calculate the epochs ratio (relation between calculated possible epochs within receiver session time and the properly registered epochs)

    Args:
        obs_times (pd.DateTimeIndex): Epochs of a given RINEX file
        min_ratio (float): Min expected ratio

    Returns:
        bool: True if ratio is equal or higher than min_ratio
    """
    if check_gps_date(rinex_epochs)[0] == 'OK':
        session_timedelta = rinex_epochs[-1] - rinex_epochs[0]
        ratio = rinex_epochs.shape[0] / (session_timedelta.total_seconds() // gps_freq)
        return ('OK', '') if ratio >= min_ratio else ('FAIL', 'Bad SEQLOG recording')
    else:
        return ('FAIL', 'Two or more days within SEQLOG')
    
if __name__ == "__main__":
    # Paths to the RTCM3 and RINEX files
    rtcm_file = "SEQLOG00.txt"
    rinex_file = "SEQLOG00.obs"
    
    # Running the functions
    parse_rtcm_to_rinex(rtcm_file)
    print('RTCM3 file successfully parsed to RINEX.')
    rinex_epochs = get_rinex_epochs(rinex_file)
    print(f'Epochs succesfully read from RINEX: {rinex_epochs.shape[0]}')
    gps_freq = check_gps_frequency(rinex_epochs)
    print(f'GPS frequency succesfully checked. Result: {gps_freq[0]}')
    gps_date = check_gps_date(rinex_epochs)
    print(f'GPS date succesfully checked. Result: {gps_date[0]}')
    rinex_ratio = check_epochs_ratio(rinex_epochs, 0.6)
    print(f'Epochs ratio succesfully checked. Result: {rinex_ratio[0]}')
