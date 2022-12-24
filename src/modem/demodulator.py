from queue import Queue
import threading
import numpy as np
import sounddevice as sd
from collections import deque
from time import time

from .soundproperties import SoundProperties

class Demodulator:
    def __init__(self, properties: SoundProperties, th0, th1):
        self.__properties = properties
        self.__th0 = th0
        self.__th1 = th1

    def closest_frequency_index(self, block_size, sample_rate, target_freq):

        deltas = float('inf')
        closest = -1

        freqs = np.fft.fftfreq(block_size, 1 / sample_rate)[:block_size // 2]

        for i in range(len(freqs)):
            if abs(freqs[i] - target_freq) < deltas:
                    deltas = abs(freqs[i] - target_freq)
                    closest = i

        return closest

    def demodulate(self,
        buffer: Queue,
        blocking: bool=False
    ):
        # run this function in a different thread
        if not blocking:
            threading.Thread(target=self.demodulate, args=(buffer, True), daemon=False).start()
            return


        subsymbol_count = 4
        
        stream = sd.InputStream(
            samplerate=self.__properties.sample_rate,
            blocksize=self.__properties.block_size,
            channels=1,
        )

        i0 = self.closest_frequency_index(self.__properties.block_size, self.__properties.sample_rate, self.__properties.f0)
        i1 = self.closest_frequency_index(self.__properties.block_size, self.__properties.sample_rate, self.__properties.f1)


        subsymbols = deque(maxlen=subsymbol_count)
        invalids = deque([-1] * subsymbol_count)


        self.__all = 0
        self.__wait = 0
        self.__stop = False
        with stream:
            while not self.__stop:

                """ if len(subsymbols) < subsymbol_count:
                    get_size = subsymbol_count - len(subsymbols)
                elif subsymbols == invalids:
                    buffer.put(-1)
                    get_size = subsymbol_count
                elif subsymbols.count(-1)

                for _ in range(get_size): """

                start = time()

                block = stream.read(self.__properties.block_size)[0]

                after_wait = time()

                self.__wait += after_wait - start

                magnitudes = abs(np.fft.rfft(block[:, 0])[:self.__properties.block_size // 2])

                if magnitudes[i0] > self.__th0 and magnitudes[i0] >= magnitudes[i1]:
                    subsymbols.append(0)
                elif magnitudes[i1] > self.__th1 and magnitudes[i1] > magnitudes[i0]:
                    subsymbols.append(1)
                else:
                    subsymbols.append(-1)

                buffer.put(subsymbols.popleft())

                self.__all += time() - start


    def stop(self):
        self.__stop = True
        print(self.__all, self.__wait)