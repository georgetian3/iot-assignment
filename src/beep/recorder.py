import wave
import pyaudio
import numpy as np
import argparse
class waveRecorder():
    def __init__(self,sampleRate,duration):
        self.sampleRate = sampleRate
        self.duration = duration
        self.filepath = 'record.wav'
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,channels=1,rate=self.sampleRate,
                            input=True,frames_per_buffer=1024)
        print('----------begin----------')
        frames = []
        for i in range(int(self.sampleRate*self.duration/1024)+1):
            data = stream.read(1024)
            frames.append(data)
        print('---------end---------')
        stream.stop_stream()
        stream.close()
        width = audio.get_sample_size(pyaudio.paInt16)
        audio.terminate()
        return np.frombuffer(b''.join(frames),dtype='<i2').reshape(-1,1),width
    def saveWave(self):
        w=wave.open(self.filepath,'wb')
        frames,width=self.record()
        w.setnchannels(2)
        w.setsampwidth(width)
        w.setframerate(self.sampleRate)
        w.writeframes(b''.join(frames))
        w.close()

