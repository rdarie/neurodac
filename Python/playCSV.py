################################
# Plays sine waves out of all channels with 10 Hz frequency
# Last Updated: 10/02/2020
# Author: Marc P. Powell
################################

import sounddevice as sd
import numpy as np
import pandas as pd
import time
from math import pi
from sys import platform
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

# Check which OS is being used
if platform == "linux" or platform == "linux2":
    # linux
    pass
elif platform == "darwin":
    # OS X
    pass
elif platform == "win32" or platform == "cygwin":
    # Windows
    pass
else:
    raise Exception('OS not understood, please use a supported OS')

# Make data to be streamed
numChannels = 8
# fs = 44100. # Hz
fs = 192000. # Hz
active_channel = 0

raw_data = pd.read_csv('./example_data/murdoc_nform_20180725.csv')

t_orig = raw_data.index / 3e4
interp_fun = interp1d(t_orig, raw_data.iloc[:, 0])
t_new = np.arange(t_orig[0], t_orig[-1], fs ** -1)
data = np.zeros([t_new.size, numChannels]) # Initialize data array

data[:, active_channel] = interp_fun(t_new)
data[:, active_channel] = data[:, active_channel] - np.mean(data[:, active_channel])
data[:, active_channel] = data[:, active_channel] / max(np.abs(data[:, active_channel].max()), np.abs(data[:, active_channel].min()))

# Get a list of the available audio devices and find the one corresponding to the neuroDAC
audioDevices = sd.query_devices()
neuroDAC_info = next((device for device in audioDevices if 'U-DAC8' in device['name']), None)
if not neuroDAC_info:
    raise Exception('No neuroDAC device detected. Please make sure device is plugged in and powered on and drivers are properly installed')

for round in range (1):
    sd.play(
        data, samplerate=fs, blocking=True,
        device=audioDevices.index(neuroDAC_info))
