import numpy as np
from queue import Queue

import sounddevice as sd

from .utils import graph

from .soundproperties import SoundProperties


class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.elements = [None] * size
        self.head = 0
        self.tail = 0 # tail is the index of the element after the last



    def append(self, x):
        self.elements[self.tail] = x

        self.tail = (self.tail + 1) % self.size

        if self.head == self.tail:
            self.head += 1

    def extend(self, xs):
        for x in xs:
            self.append(x)
    
    def view(self, start, stop=None):
        if not 0 <= start < self.size:
            raise ValueError('Start out of bounds')
        if stop == None:
            return self.elements[self.head]
        if not start <= stop <= self.size:
            raise ValueError('End out of bounds')

        i1 = (self.head + start) % self.size
        i2 = (self.head + stop) % self.size



        if (i1 >= i2):
            return self.elements[i1:] + self.elements[:i2]
        else:
            return self.elements[i1:i2]

    def __str__(self):
        return str(self.view(0, self.size))


import sys

import threading

class Demodulator:
    def __init__(self, properties: SoundProperties):
        """
        `properties`: physical properties of the sound wave to be received and demodulated
        """
        self.p = properties
        self.buffer = Queue(1024)
        self.__stop = False

    def closest_frequency_index(self, blocksize, target_freq):

        deltas = float('inf')
        closest = -1

        freqs = np.fft.fftfreq(blocksize, 1 / self.p.sample_rate)[:blocksize // 2]

        for i in range(len(freqs)):
            if abs(freqs[i] - target_freq) < deltas:
                    deltas = abs(freqs[i] - target_freq)
                    closest = i

        return closest



    def demodulate(self, bit_buffer: list, blocksize: int, blocking: bool=False):
        # run this function in a different thread
        if not blocking:
            threading.Thread(target=self.demodulate, args=(bit_buffer, blocksize, True,), daemon=False).start()
            return

        stream = sd.InputStream(
            samplerate=self.p.sample_rate,
            blocksize=blocksize,
            channels=1,
        )

        i0 = self.closest_frequency_index(blocksize, self.p.f0)
        i1 = self.closest_frequency_index(blocksize, self.p.f1)

        with stream:
            while not self.__stop:
                indata = stream.read(blocksize)[0]
                magnitudes = abs(np.fft.rfft(indata[:, 0])[:blocksize // 2])
                if magnitudes[i0] > self.p.th0 and magnitudes[i0] >= magnitudes[i1]:
                    print(0, end='')
                elif magnitudes[i1] > self.p.th1 and magnitudes[i1] > magnitudes[i0]:
                    print(1, end='')
                else:
                    print(' ', end='')
                sys.stdout.flush()

    def stop(self):
        self.__stop = True

