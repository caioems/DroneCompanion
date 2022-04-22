# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: T2
"""

import os
import numpy as np
import pandas as pd
from pymavlink.mavextra import *
from pymavlink import mavutil

log_path = "C:/temp.csv"
with open(log_path, mode='r') as f:
    df = pd.read_csv(f)       
    f.close()




                     