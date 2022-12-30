import socket  	
import scipy.signal
import numpy as np
import sounddevice as sd
import recorder
from threading import Thread
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        super(ThreadWithReturnValue,self).join()
        return self._return
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = ''
port = 2333
socket_server.bind((host,port))
socket_server.listen(5)
client_socket ,address = socket_server.accept()

def receive_time():
    data = client_socket.recv(1024)          #获取客户端请求的数据
    client_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\nHello World')    
    return float(data.decode('utf-8'))
def send_ready():
    client_socket.sendall(b'server ready')
    data = client_socket.recv(1024).decode('utf-8')
    if data == 'client ready':
        return True
    else:
        return False
def filter_bp(x,fs,wl,wh):
    fN = 3
    fc = fs/2
    w1c = wl/fc
    w2c = wh/fc
    b, a = signal.butter(fN,[w1c, w2c],'bandpass')
    x_filter = signal.filtfilt(b,a,x)
    return x_filter

if __name__ == '__main__':
    fs = 48000
    T = 0.5
    f1 = 4000
    f2 = 6000
    f3 = 8000
    t = np.linspace(0,T,round(fs*T))
    y = scipy.signal.chirp(t,f1,T,f2)
    if(send_ready()):
        r = recorder.waveRecorder(fs,6*T,'sender.wav')
        thread = ThreadWithReturnValue(target=r.saveWave)
        thread.start()
        sd.play(y, fs,blocking=True)
        data  = thread.join()
        data  = filter_bp(data.reshape(-1),fs,3500,8500)
        z1 = scipy.signal.chirp(t,f1,T,f2)
        z2 = scipy.signal.chirp(t,f2,T,f3)
        z1 = z1[::-1]
        z2 = z2[::-1]

        c1 = np.convolve(data,z1.reshape(-1),'valid')
        p1 = np.argmax(c1)
        p2 = np.argmax(np.convolve(data,z2.reshape(-1),'valid'))

        psub = receive_time()
        psub = psub/fs
        plt.plot(data)
        plt.axvline(p1,c='r')
        plt.axvline(p2)
        plt.savefig('sender.png')
        p1 = (p1-1)/fs
        p2 = (p2-1)/fs
        dAA = 0
        dBB = 0
        print(p1,p2,psub)
        print('结果(m)：')
        print(343 / 2 * (p2 - p1 - psub) + dAA + dBB)