import numpy as np
import random
from queue import Queue
from .bluetooth import BluetoothSender, BluetoothReceiver

def add_random_noise(wave):
    noise = np.random.normal(0,1,100)
    wave += noise

class Tester:

    def __init__(self, sender: BluetoothSender=None, receiver: BluetoothReceiver=None):
        if sender:
            self.sender = sender
            #self.modulator = sender.__modulator
        elif receiver:
            self.receiver = receiver
            #self.demodulator = receiver.__demodulator
        else:
            raise ValueError('Either sender or receiver must be specified')

    def run(self):

        text = 'test'
        data = text.encode('utf8')
        if self.receiver:
            text_buffer = Queue()
            self.receiver.receive(text_buffer)
        if self.sender:
            self.sender.send(data, blocking=True)