import numpy as np
from scipy import signal

N = 2
Wnl = 0.02
bl, al = signal.butter(N, Wnl, btype="lowpass")
Wnb = (0.02,0.05)
bb, ab = signal.butter(N, Wnb, btype="bandpass")
Wnh = 0.05
bh, ah = signal.butter(N, Wnh, btype="highpass")

def lp_filter(input_signal):
    """Passes input signal through a Nth low pass filter of parameters al and bl."""
    # print("at lp filter")
    return signal.filtfilt(bl, al, input_signal)  

def bp_filter(input_signal):
    """Passes input signal through a Nth band pass filter of parameters ab and bb."""
    # print("at bp filter")
    return signal.filtfilt(bb, ab, input_signal)

def hp_filter(input_signal):
    """Passes input signal through a Nth high pass filter of parameters ah and bh."""
    # print("at hp filter")
    return signal.filtfilt(bh, ah, input_signal)


def get_volume(signal):
    """Returns volume (integer) given a signal"""
    # print("at get volume")
    peak=np.average(np.abs(signal))/10000
    volume=int(peak/1000)
    return volume

def print_volume(signal, signal_label):
    """Uses get_volume() to print volume in #'s.
    Can add a signal_label that is printed before the volume."""
    # print("at print volume")
    bars = "#"*get_volume(signal)
    print("%s %s"%(signal_label,bars))

def get_low_volume(signal):
    """Gets volume of signal after passing it through a low pass filter"""
    return get_volume(lp_filter(signal))

def get_band_volume(signal):
    """Gets volume of signal after passing it through a band pass filter"""
    return get_volume(bp_filter(signal))

def get_high_volume(signal):
    """Gets volume of signal after passing it through a high pass filter"""
    return get_volume(hp_filter(signal))


def show_volume_as_colored_bars(volume):
    """Volume visualized as bars of different colors"""

    # volume=np.sum(data_array)/2**22
    # bars=int(volume/2**10)

    volume -= 20
    black_bar = [[0,0,0]]*8
    blue_bar = [[0,0,255]]*8
    red_bar = [[255,0,0]]*8
    cyan_bar = [[0,255,255]]*8
    yellow_bar = [[255,255,0]]*8
    white_bar = [[255,255,255]]*8
    if volume<=0:
        return 8*black_bar
    elif volume<=8:
        return (8-volume)*black_bar + volume*blue_bar
    elif volume<=16:
        volume -= 8
        return (8-volume)*blue_bar + volume*red_bar
    elif volume<=24:
        volume -= 16
        return (8-volume)*red_bar + volume*cyan_bar
    elif volume<=32:
        volume -= 24
        return (8-volume)*cyan_bar + volume*yellow_bar
    elif volume<=40:
        volume -= 32
        return (8-volume)*yellow_bar + volume*white_bar
    else:
        return 8*white_bar

def show_volume_as_colors(volume):
    """Sets display color accourding to volume level. 
    Returns a list of 64 color lists."""
    # volume=np.sum(data_array)/2**22
    volume *= 100
    red_level = int(volume % 255)
    blue_level = int((volume//2) % 255)
    green_level = int((volume//5) % 255)
    color = [red_level, green_level, blue_level]

    return [color]*64

def get_intensity_from_volume(volume, max_volume=60):
    """Outputs the LED intensity(min 0, max 255) from input volume.
    Max volume can be set (default value is 60). Increasing the max volume 
    will decrease the LED intensity."""
    # max_volume = 60
    if volume < max_volume:
        intensity = (volume * 255) // max_volume
    else:
        intensity = 255
    return intensity

def show_frequency_as_colors(l_volume, b_volume, h_volume):
    """Changes colors (increasing volume increases intensity) depending upon
    volumes of low pass, band pass, high pass filter output."""
    color = [get_intensity_from_volume(l_volume), get_intensity_from_volume(b_volume), get_intensity_from_volume(h_volume)]
    return [color]*64


if __name__ == "__main__":
    print(volume_as_colors(172941))
    for i in range(10000):
        print(volume_as_colors(i)[0])
