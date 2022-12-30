import socket  	
import scipy.signal
import numpy as np
import sounddevice as sd
import recorder
from threading import Thread
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
if __name__ == '__main__':
    fs = 48000
    T = 0.5
    f1 = 4000
    f2 = 6000
    f3 = 8000
    t = np.linspace(0,T,round(fs*T))
    y = scipy.signal.chirp(t,f1,T,f2)
    if(send_ready()):
        r = recorder.waveRecorder(fs,3)
        thread = ThreadWithReturnValue(target=r.saveWave)
        thread.start()
        sd.play(y, fs,blocking=True)
        data  = thread.join()

        z1 = scipy.signal.chirp(t,f1,T,f2)
        z2 = scipy.signal.chirp(t,f2,T,f3)
        z1 = z1[::-1]
        z2 = z2[::-1]
        psub = receive_time()
        psub = psub/fs
        c1 = np.convolve(data.reshape(-1),z1.reshape(-1),'valid')
        p1 = np.argmax(c1)
        p2 = np.argmax(np.convolve(data.reshape(-1),z2.reshape(-1),'valid'))

        
        plt.plot(data.reshape(-1))
        plt.axvline(p1,c='r')
        plt.axvline(p2)
        plt.show()
        p1 = (p1-1)/fs
        p2 = (p2-1)/fs
        dAA = 0.2
        dBB = 0.2
        print(p1,p2,psub)
        print(343 / 2 * (p2 - p1 - psub) + dAA + dBB)