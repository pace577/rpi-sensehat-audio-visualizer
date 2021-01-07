#!/usr/bin/python3

"""
                      ____ _____ _____
 _ __   __ _  ___ ___| ___|___  |___  |
| '_ \ / _` |/ __/ _ \___ \  / /   / /
| |_) | (_| | (_|  __/___) |/ /   / /
| .__/ \__,_|\___\___|____//_/   /_/
|_|

Play input audio and visualize fft volume on a Raspberry Pi SenseHAT.

"""

import sys
import wave
import pyaudio
import numpy as np
from scipy import signal
from sense_hat import SenseHat
from utils import *

# Path to input audio file. Can also give as argument to the program
filename = "samples/music.wav"
if len(sys.argv)>1:
    filename = sys.argv[1]
wf = wave.open(filename)
sense = SenseHat()

# The audio is read and processed in chunks
CHUNK = 2**11
RATE = wf.getframerate()

# Design filters
# 600Hz - Low pass cutoff
# 2500Hz - High pass cutoff
# 600Hz-2500Hz - Band pass range

N = 2
Wnl = 600/RATE
Wnh = 2500/RATE
Wnb = (Wnl,Wnh)

# AudioVisualizer uses audio data to make LEDs on SenseHAT glow
vis = AudioVisualizer(memory=5, max_volume=60, responsiveness=4)
vis.set_filter(N=N,Wn=[Wnl,Wnh,Wnb])

# Start audio stream
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,
              channels=wf.getnchannels(),
              rate=RATE,
              output=True,
              frames_per_buffer=CHUNK)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    audio_as_np_int = np.frombuffer(data, dtype=np.int)
    data_array = audio_as_np_int.astype(np.float)

    # Print volume in terminal (for debugging)
    #vis.print_volume_after_filter(data_array, ["low ", "high ", "band "])

    sense.set_pixels(vis.show_frequency_as_colors(data_array))
    #sense.set_pixels(show_volume_as_colors(get_volume(data_array)))
    data = wf.readframes(CHUNK)
    

stream.close()
p.terminate()
