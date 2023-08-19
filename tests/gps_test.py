import os
import georinex as gr
import pandas as pd
from pyrtcm import RTCMReader


def convert_rtcm_to_rinex(rtcm_file):
    """
    Function to convert the RTCM3 file to RINEX obs file using the CONVBIN tool from RTKLIB.
    
    :param rtcm_file: Path to the RTCM3 file.
    """
    # Verify if the RTCM3 file exists
    if not os.path.exists(rtcm_file):
        raise FileNotFoundError(f"RTCM3 file not found: {rtcm_file}")

    try:
        command = f"convbin.exe -r rtcm3 {rtcm_file}"
        os.system(command)
    except:
        print("RTCM3 file could not be converted.")

#TODO: fix this method (the datetime conversion is not working)        
def convert_rtcm_to_dataset(rtcm_file):
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
                yield parsed_data.GNSSEpoch
            except AttributeError:
                continue
            
    epochs_list = list(epochs_yield())
    return epochs_list
            
#TODO: check and compare times of different logs
def get_rinex_times(rinex_file):
    """
    Function to get the observations time of a rinex file.
    :param rinex_file: Path to the RINEX obs file.
    """
    if not os.path.exists(rinex_file):
        raise FileNotFoundError(f"RINEX file not found: {rinex_file}")
    
    r_times = gr.obstime3(rinex_file)
    os.remove(rinex_file)
    return r_times

def check_obs_frequency(obs_times):
    """
    Function that compares the time of two consecutive observations 
    in order to check the observations frequency.
    
    :param obs_times: numpy.ndarray containing the datetime of each observation.
    """

    if pd.Timedelta(microseconds=199999) <= pd.Series(obs_times).diff().median() <= pd.Timedelta(microseconds=200001):
        return True
    else:
        return False
    
def check_obs_period(obs_times):
    """
    Function that check the period (days) of the observations. If there are
    observations from different days within the log, returns false.
    
    :param obs_times: array containing the datetime of each observation.
    """
    days = pd.DataFrame([dt.day for dt in obs_times])
    if days.nunique()[0] == 1:
        return True
    else:
        return False  

if __name__ == "__main__":
    # Paths to the RTCM3 and RINEX files
    rtcm_file = "SEQLOG00.txt"
    rinex_file = "SEQLOG00.obs"
    
    # Running the functions
    convert_rtcm_to_rinex(rtcm_file)
    print('RTCM3 file successfully converted to RINEX.')
    obs_times = get_rinex_times(rinex_file)
    print('Observations succesfully taken from RINEX.')
    obs_freq = check_obs_frequency(obs_times)
    print('Observations frequency succesfully checked.')
    obs_period = check_obs_period(obs_times)
    print('Observations period succesfully checked.')
