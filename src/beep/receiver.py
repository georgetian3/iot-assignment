import socket  	
import scipy.signal
import numpy as np
import sounddevice as sd
import recorder
from threading import Thread
from scipy.io import wavfile
import time
import matplotlib.pyplot as plt
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "127.0.0.1"
port = 2333
client.connect((host,port))
class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        super(ThreadWithReturnValue,self).join()
        return self._return
def sendTime(time):
    send_msg = str(time)
    client.send(send_msg.encode('utf-8'))
    msg = client.recv(1024)
    print(f'receive msg : {msg.decode("utf-8")}')
def getmsg():
    msg = client.recv(1024).decode('utf-8')
    if msg == 'server ready':
        client.send('client ready'.encode('utf-8'))
        return msg
if __name__ == '__main__':
    if (getmsg() == 'server ready'):
        fs = 48000
        T = 0.5
        f1 = 4000
        f2 = 6000
        f3 = 8000
        t = np.linspace(0,T,round(fs*T))
        y = scipy.signal.chirp(t,f2,T,f3)
        r = recorder.waveRecorder(fs,3)
        thread = ThreadWithReturnValue(target=r.saveWave)
        thread.start()
        time.sleep(1)
        sd.play(y, fs,blocking=True)
        data = thread.join()
        z1 = scipy.signal.chirp(t,f1,T,f2)
        z2 = scipy.signal.chirp(t,f2,T,f3)
        z1 = z1[::-1]
        z2 = z2[::-1]
        p1 = np.argmax(np.convolve(data.reshape(-1),z1.reshape(-1),'valid'))
        p2 = np.argmax(np.convolve(data.reshape(-1),z2.reshape(-1),'valid'))
        print(data.shape)
        plt.plot(data.reshape(-1))
        plt.axvline(p1,c='r')
        plt.axvline(p2)
        plt.show()
        print(343*p1/fs)
        print(p2,p1)
        print((p2-p1)/fs)
	
        sendTime(p2-p1)
        client.close()
