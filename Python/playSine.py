################################
# Plays sine waves out of all channels with 10 Hz frequency
# Last Updated: 10/02/2020
# Author: Marc P. Powell
################################

import sounddevice as sd
import numpy
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
fs = 44100. # Hz
duration = 20. # sec

t = numpy.arange(0, duration, 1/fs)
freq = numpy.array([100] * 8) # Frequency of each channel (Hz)
amp = numpy.array([1] * 8) # Amplitude of each channel (-1 -> 1)

numSamps = t.size
numChannels = 8
data = numpy.zeros([numSamps, numChannels]) # Initialize data array
for channel in range(numChannels):
    data[:, channel] = amp[channel]*numpy.sin(2*pi*freq[channel]*t)

# Play the data!
print('Starting to play')
sd.play(
    data, samplerate=fs, blocking=True,
    device=audioDevices.index(neuroDAC_info))
print('Done')
