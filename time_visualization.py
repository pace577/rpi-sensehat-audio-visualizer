import sys
import pyaudio
import wave
import numpy as np
from sense_hat import SenseHat
from utils import *


FILENAME = "samples/music.wav"
if len(sys.argv)>1:
    FILENAME = sys.argv[1]
wf = wave.open(FILENAME, 'rb')

CHUNK = 2**12
RATE = wf.getframerate()
CHANNELS = wf.getnchannels()

sense = SenseHat()

p=pyaudio.PyAudio()
stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    audio_as_np_int= np.frombuffer(data, dtype=np.int)
    data_array = audio_as_np_int.astype(np.float)

    sense.set_pixels(show_volume_as_colors(get_volume(data_array)))
    data = wf.readframes(CHUNK)


# stream.stop_stream()
stream.close()
p.terminate()
