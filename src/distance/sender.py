import socket  	
import scipy.signal
import numpy as np
import sounddevice as sd
from . import recorder
from threading import Thread
from scipy import signal
import matplotlib.pyplot as plt
class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        super(ThreadWithReturnValue,self).join()
        return self._return

class Sender:
    def __init__(self,port,dAA,dBB):
        self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = ''
        self.port = port
        self.dAA = dAA
        self.dBB = dBB
        self.socket_server.bind((self.host,self.port))
        self.socket_server.listen(5)
        self.client_socket ,self.address = self.socket_server.accept()

    def receive_time(self):
        data = self.client_socket.recv(1024)          
        return float(data.decode('utf-8'))
    def send_ready(self):
        self.client_socket.sendall(b'server ready')
        data = self.client_socket.recv(1024).decode('utf-8')
        if data == 'client ready':
            return True
        else:
            return False
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
        T =  0.5
        f1 = 4000
        f2 = 6000
        f3 = 8000
        t = np.linspace(0,T,round(fs*T))
        y = scipy.signal.chirp(t,f1,T,f2)
        if(self.send_ready()):
            r = recorder.waveRecorder(fs,6*T,'sender.wav')
            thread = ThreadWithReturnValue(target=r.saveWave)
            thread.start()
            sd.play(y, fs,blocking=True)
            data  = thread.join()
            data  = self.filter_bp(data.reshape(-1)[:int(6*T*fs)],fs,f1-10,f3+10)
            z1 = scipy.signal.chirp(t,f1,T,f2)
            z2 = scipy.signal.chirp(t,f2,T,f3)
            z1 = z1[::-1]
            z2 = z2[::-1]

            p1 = np.argmax(np.convolve(data,z1.reshape(-1),'valid'))
            p2 = np.argmax(np.convolve(data,z2.reshape(-1),'valid'))

            psub = self.receive_time()
            psub = psub/fs

            plt.plot(data)
            plt.axvline(p1,c='r')
            plt.axvline(p2)
            plt.savefig('sender.png')

            print('结果(cm)：')
            result = 100* 343/2 * ( p2 - p1 - psub) + self.dAA + self.dBB
            print(result)