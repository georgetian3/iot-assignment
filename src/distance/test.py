import numpy as np
import random


class Tester:

    def __init__(self, sender=None, receiver=None):
        if sender:
            self.sender = sender
            self.modulator = sender.__modulator
        elif receiver:
            self.receiver = receiver
            self.demodulator = receiver.__demodulator
        else:
            raise ValueError('Either sender or receiver must be specified')

    def run(self):
        text = random.randint()
        pass