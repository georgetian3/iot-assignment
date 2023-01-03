import socket  	
import scipy.signal
import numpy as np
import sounddevice as sd
from . import recorder
from scipy import signal
from threading import Thread
import time
import matplotlib.pyplot as plt

class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        super(ThreadWithReturnValue,self).join()
        return self._return
class Receiver:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.host,self.port))
    def sendTime(self,time):
        send_msg = str(time)
        self.client.send(send_msg.encode('utf-8'))
        msg = self.client.recv(1024)
        print(f'receive msg : {msg.decode("utf-8")}')
    def getmsg(self):
        msg = self.client.recv(1024).decode('utf-8')
        if msg == 'server ready':
            self.client.send('client ready'.encode('utf-8'))
            return True
    def filter_bp(self,x,fs,wl,wh):
        fN = 3
        fc = fs/2
        w1c = wl/fc
        w2c = wh/fc
        b, a = signal.butter(fN,[w1c, w2c],'bandpass')
        x_filter = signal.filtfilt(b,a,x)
        return x_filter
    def main(self):
        fs = 48000
        T = 0.5
        f1 = 4000
        f2 = 6000
        f3 = 8000
        t = np.linspace(0,T,round(fs*T))
        y = scipy.signal.chirp(t,f2,T,f3)
        if (self.getmsg()):
            r = recorder.waveRecorder(fs,6*T,'receiver.wav')
            thread = ThreadWithReturnValue(target=r.saveWave)
            thread.start()
            time.sleep(3*T)
            sd.play(y, fs)
            data = thread.join()
            data = self.filter_bp(data.reshape(-1)[:int(6*T*fs)],fs,f1-10,f3+10)
            z1 = scipy.signal.chirp(t,f1,T,f2)
            z2 = scipy.signal.chirp(t,f2,T,f3)
            z1 = z1[::-1]
            z2 = z2[::-1]
            p1 = np.argmax(np.convolve(data,z1.reshape(-1),'valid'))
            p2 = np.argmax(np.convolve(data,z2.reshape(-1),'valid'))
            self.sendTime(p2-p1)
            plt.plot(data)
            plt.axvline(p1,c='r')
            plt.axvline(p2,c='g')
            plt.savefig('receiver.png')
            print(343*p1/fs)
            print((p2-p1)/fs)
        self.client.close()
