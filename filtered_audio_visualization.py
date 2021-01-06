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
from sense_hat import SenseHat
from utils import *

filename = "samples/music.wav"
if len(sys.argv)>1:
    filename = sys.argv[1]
wf = wave.open(filename)
sense = SenseHat()

CHUNK = 2**11
RATE = wf.getframerate()

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

    # print_volume(lp_filter(data_array), "low "+str(i))
    # print_volume(bp_filter(data_array), "band "+str(i))
    # print_volume(hp_filter(data_array), "high "+str(i))

    sense.set_pixels(show_frequency_as_colors(get_low_volume(data_array),
                    get_band_volume(data_array),
                    get_high_volume(data_array)))
    # sense.set_pixels(show_volume_as_colors(get_volume(data_array)))
    data = wf.readframes(CHUNK)
    

stream.close()
p.terminate()
