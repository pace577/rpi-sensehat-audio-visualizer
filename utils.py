import numpy as np
from scipy import signal

# def filter_signal(input_signal, b, a):
#     """Passes input signal through a Nth low pass filter of parameters al and bl."""
#     signal.filtfilt(b, a, signal)
#     # print("at lp filter")
#     return 

# def lp_filter(input_signal):
#     """Passes input signal through a Nth low pass filter of parameters al and bl."""
#     # print("at lp filter")
#     return signal.filtfilt(bl, al, input_signal)  

# def bp_filter(input_signal):
#     """Passes input signal through a Nth band pass filter of parameters ab and bb."""
#     # print("at bp filter")
#     return signal.filtfilt(bb, ab, input_signal)

# def hp_filter(input_signal):
#     """Passes input signal through a Nth high pass filter of parameters ah and bh."""
#     # print("at hp filter")
#     return signal.filtfilt(bh, ah, input_signal)

class AudioVisualizer:
    def __init__(self, max_volume=60, memory=3, responsiveness=3):
        """
        AudioVisualizer class to visualize audio using Raspberry Pi SenseHAT LED grid.
        - Increasing the Max volume decreases intensity
        - Increasing memory makes the response smoother (increases width of
          moving average filter)
        - Increasing responsiveness increases the weight added to current volume
          input (amplitude of initial value in the moving average filter)
         
         Before using show_frequency_as_colors, you must set a triple filter
         (consists of a low pass, band pass and a high pass butterworth filter)
         using set_filter(). 

         No filter is required for show_volume_as_colored_bars() and
         show_volume_as_colors().

         How it works (taking show_frequency_as_colors() as an example):
         - get_volume_after_filter calculates volume of the input audio chunk
         - smoothen_volume() filters the volume signal using a moving average
           filter
         - get_intensity_from_volume() returns the intensity value for each of
           the RGB LEDs in the Sense HAT. This can be given as input to the
           SenseHAT object in your program.
        """
        self.a = [0,0,0]
        self.b = [0,0,0]
        self.max_volume = max_volume
        self.memory = memory
        self.volume_array = np.zeros((memory,3))
        self.responsiveness = responsiveness


    def set_filter(self, N=3, Wn=[0.01, 0.5, (0.01,0.5)]):
        """Set single filter or triple filter"""
        if type(Wn) is float:
            self.b, self.a = signal.butter(N, Wn, btype="lowpass")
            self.filter_num = 'single'
        elif type(Wn) is list and len(Wn) == 3:
            self.b[0], self.a[0] = signal.butter(N, Wn[0], btype="lowpass")
            self.b[1], self.a[1] = signal.butter(N, Wn[1], btype="highpass")
            self.b[2], self.a[2] = signal.butter(N, Wn[2], btype="bandpass")
            self.filter_num = 'triple'
        else:
            self.filter_num = None


    def set_max_volume(self, max_volume):
        """Increasing the max volume decreases the intensity of colors on LED"""
        self.max_volume = max_volume


    def get_volume(self, audio):
        """Returns volume (integer) given a audio"""
        # print("at get volume")
        peak=np.average(np.abs(audio))/10000
        volume=int(peak/1000)
        return volume


    def print_volume(self, audio, audio_label):
        """Uses get_volume() to print volume in #'s.
        Can add a audio_label that is printed before the volume."""
        # print("at print volume")
        bars = "#"*self.get_volume(audio)
        print("%s %s"%(audio_label,bars))


    def get_volume_after_filter(self, audio):
        """Gets volume of audio after passing it through a low pass filter.  

        Inputs: audio signal (mono), numerator (b) and denominator(a) coefficients
        of filter.
        If b (and a) is a list of coefficients, the function passes the
        input audio through a list of corresponding filters and returns a list of
        volumes."""
        if self.filter_num == 'single':
            return self.get_volume(signal.filtfilt(self.b, self.a, audio))
        elif self.filter_num == 'triple':
            return [self.get_volume(signal.filtfilt(self.b[i], self.a[i], audio)) for i in range(3)]
        else:
            return -1


    def print_volume_after_filter(self, audio, audio_label):
        """Uses get_volume_after_filter() to print volume(s) in #'s.
        Can add audio_label(s) that is printed before the volume.

        Inputs: mono audio signal (np.ndarray), 
                filter numerator coefficients b (np.ndarray or list of arrays),
                filter denominator coefficients a (np.ndarray or list of arrays),
                audio prefix labels to print to console (string or list of strings)
        """
        #print("at print volume")
        volume = self.get_volume_after_filter(audio)
        if self.filter_num == 'single':
            bars = "#"*volume
            print("%s %s"%(audio_label,bars))
        elif self.filter_num == 'triple':
            for i in range(len(volume)):
                bars = "#"*volume[i]
                print("filter%d %s %s"%(i,audio_label[i],bars))
        else:
            return -1


    def show_volume_as_colored_bars(self, audio):
        """Volume visualized as bars of different colors"""

        volume = self.get_volume(audio)
        #volume=np.sum(audio)/2**22
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


    def show_volume_as_colors(self, audio):
        """Sets display color accourding to volume level. 
        Returns a list of 64 color lists."""
        #volume=np.sum(audio)/2**22
        volume = 100*self.get_volume(audio)
        red_level = int(volume % 255)
        blue_level = int((volume//2) % 255)
        green_level = int((volume//5) % 255)
        color = [red_level, green_level, blue_level]

        return [color]*64


    def get_intensity_from_volume(self, volume):
        """Outputs the LED intensity(min 0, max 255) from input volume.
        Max volume can be set (default value is 60). Increasing the max volume 
        will decrease the LED intensity."""
        if volume < self.max_volume:
            intensity = (volume * 255) // self.max_volume
        else:
            intensity = 255
        return intensity


    def smoothen_volume(self, volume):
        """This is essentially a moving average filter to the volume signal.
        Responsiveness is the weight added to current volume input."""
        volume = np.array(volume)
        self.volume_array = self.volume_array[1:]
        #print("Volume array after slicing:", self.volume_array)

        weight = self.responsiveness #current volume adds extra weight to the visuals
        normalized_volume = np.average(np.vstack((self.volume_array,weight*volume)), axis=0)
        #print("Normalized volume: ", normalized_volume)

        self.volume_array = np.vstack((self.volume_array, volume))
        #print("Volume array after stacking:", self.volume_array)
        return normalized_volume.astype(int)


    def show_frequency_as_colors(self, audio):
        """Changes colors (increasing volume increases intensity) depending upon
        volumes of low pass, band pass, high pass filter output."""

        if self.filter_num == 'triple':
            volume = self.get_volume_after_filter(audio)
            volume = self.smoothen_volume(volume)
            color = [self.get_intensity_from_volume(volume[i]) for i in range(3)]
            return [color]*64
        else:
            return -1


if __name__ == "__main__":
    print(volume_as_colors(172941))
    for i in range(10000):
        print(volume_as_colors(i)[0])
