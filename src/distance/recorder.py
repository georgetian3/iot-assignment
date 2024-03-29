import wave
import pyaudio
import numpy as np
import argparse
class waveRecorder():
    def __init__(self,sampleRate,duration,filepath):
        self.sampleRate = sampleRate
        self.duration = duration
        self.filepath = filepath
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt32,channels=1,rate=self.sampleRate,
                            input=True,frames_per_buffer=1024)
        print('----------begin----------')
        frames = []
        for i in range(int(self.sampleRate*self.duration/1024)+1):
            data = stream.read(1024)
            frames.append(data)
        print('---------end---------')
        stream.stop_stream()
        stream.close()
        width = audio.get_sample_size(pyaudio.paInt32)
        audio.terminate()
        return frames,width 
    def saveWave(self):
       # w=wave.open(self.filepath,'wb')
        frames,width=self.record()
        # w.setnchannels(1)
        # w.setsampwidth(width)
        # w.setframerate(self.sampleRate)
        # w.writeframes(b''.join(frames))
        # w.close()
        return  np.frombuffer(b''.join(frames),dtype='<i4').reshape(-1,1)
