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

filename = "samples/music.wav"
if len(sys.argv)>1:
    filename = sys.argv[1]
wf = wave.open(filename)
sense = SenseHat()

CHUNK = 2**11
RATE = wf.getframerate()

# Design filters
# 600Hz - Low pass cutoff
# 2500Hz - High pass cutoff
# 600Hz-2500Hz - Band pass range

N = 2
Wnl = 600/RATE
# bl, al = signal.butter(N, Wnl, btype="lowpass")
Wnh = 2500/RATE
# bh, ah = signal.butter(N, Wnh, btype="highpass")
Wnb = (Wnl,Wnh)
# bb, ab = signal.butter(N, Wnb, btype="bandpass")

# Start AudioVisualizer
vis = AudioVisualizer(memory=3, max_volume=55)
# vis.set_filter(Wn=[600/RATE, 2500/RATE, (600/RATE, 2500/RATE)])
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
    #print_volume_after_filter(data_array, bl, al, "low ")
    #print_volume_after_filter(data_array, bb, ab, "band ")
    #print_volume_after_filter(data_array, bh, ah, "high ")
    vis.print_volume_after_filter(data_array, ["low ", "high ", "band "])

    sense.set_pixels(vis.show_frequency_as_colors(
                    # get_volume_after_filter(data_array, bl, al),    #red
                    # get_volume_after_filter(data_array, bh, ah),    #green
                    # get_volume_after_filter(data_array, bb, ab)))   #blue
                    data_array))    #red
    #sense.set_pixels(show_volume_as_colors(get_volume(data_array)))
    data = wf.readframes(CHUNK)
    

stream.close()
p.terminate()
