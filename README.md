# Audio Visualizer with Raspberry Pi Sense HAT

## Requirements and Dependencies
You obviously need a Raspberry Pi, and the Sense HAT
Python libraries:
- Sense HAT module
- pyaudio
- numpy
- scipy (for signal processing)
- wave (to read .wav files)

## Usage
Plug in your Sense HAT and run the following from your Raspberry Pi. Only .wav
files are currently supported.

``` bash
python3 filtered_audio_visualization.py <path_to_audio_file>
```
