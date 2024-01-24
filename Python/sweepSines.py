################################
# Plays sine waves out of all channels with 10 Hz frequency
# Last Updated: 10/02/2020
# Author: Marc P. Powell
################################

import sounddevice as sd
import numpy as np
import time
from math import pi
from sys import platform

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

# Get a list of the available audio devices and find the one corresponding to the neuroDAC
audioDevices = sd.query_devices()

neuroDAC_info = next((device for device in audioDevices if 'U-DAC8' in device['name']), None)
if not neuroDAC_info:
    raise Exception('No neuroDAC device detected. Please make sure device is plugged in and powered on and drivers are properly installed')


# Make data to be streamed
numChannels = 8
# fs = 44100. # Hz
fs = 192000. # Hz
inset_duration = 0.05
min_duration = 3.
pause_duration = 2.
min_num_cycles_per_freq = 100

active_channel = 0
amp = 1. # Amplitude of each channel (-1 -> 1)
freqs_to_sweep = np.logspace(np.log10(.5), np.log10(15e3), 100)
all_durations = [min_num_cycles_per_freq * f ** -1 + min_duration + pause_duration for f in freqs_to_sweep]
print(f'The sweep is projected to last {np.sum(all_durations) / 60:.1f} minutes.')

for freq in freqs_to_sweep:
    period = freq ** -1
    duration = min_duration + 2 * inset_duration + min_num_cycles_per_freq * period # sec
    t = np.arange(0, duration, fs ** -1)
    data = np.zeros([t.size, numChannels]) # Initialize data array

    ## create a pulse at the begining and end of each freq
    data[:, active_channel] = 1.2 * amp
    active_mask = (t >= inset_duration) & (t <= (duration - inset_duration))
    t_sine = t[active_mask]
    t_sine -= t_sine[0]
    data[active_mask, active_channel] = amp * np.sin(2 * pi * freq * t_sine)
    # Play the data!
    print(f'Starting to play f={freq:.1f} Hz for a duration of {duration / 60:.1f} min.')
    sd.play(
        data, samplerate=fs, blocking=True,
        device=audioDevices.index(neuroDAC_info))
    print('Done')
    time.sleep(pause_duration)
