import pyaudio

pa = pyaudio.PyAudio()
pa.get_default_output_device_info()