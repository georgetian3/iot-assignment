import numpy as np
import random
from queue import Queue
from .bluetooth import BluetoothSender, BluetoothReceiver
from .modem import Modulator, Demodulator
from .soundproperties import SoundProperties
from bitarray import bitarray
import time
import difflib

def add_random_noise(wave):
    noise = np.random.normal(0,1,100)
    wave += noise

class Tester:

    def __init__(self, properties: SoundProperties, role: str):
        if role not in ['sender', 'receiver']:
            raise ValueError('Invalid role')
        self.role = role
        self.properties = properties
        self.sender = BluetoothSender(Modulator(properties))
        self.receiver = BluetoothReceiver(Demodulator(properties))

    def run(self, repeats=10):
        test_data = bitarray([0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1] * 100)
        for _ in range(len(repeats)):
            if self.role == 'receiver':
                bit_buffer = Queue()
                self.receiver.receive(bit_buffer, blocking=True)
                received_data = bitarray(bit_buffer.queue)
                assert test_data == received_data
            elif self.role == 'sender':
                self.sender.send(test_data, blocking=True)
                time.sleep(1)