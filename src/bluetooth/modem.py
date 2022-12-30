from collections import deque
from queue import Queue
from typing import Iterable
import threading
import numpy as np
import sounddevice as sd
from .soundproperties import SoundProperties

class Modulator:
    def __init__(self, properties: SoundProperties):
        self.p = properties

        self.waves = tuple(
            np.sin(
                2 * np.pi * freq *
                np.arange(self.p.block_size * self.p.blocks_per_symbol)
                / self.p.sample_rate
            ) for freq in self.p.frequencies
        )

    def modulate(self, bits: Iterable, blocking: bool=False) -> None:
        """
        Modulates the given data into a sound wave
        Parameters:
            - `bits`: Iterable where each element is a truthy or falsy value, representing `1` and `0` bits, respectively
            - `blocking`: parameter for `sounddevice.play`
        """
        symbols = []

        bits_per_symbol = int(np.log2(len(self.waves)))
        
        # combining consecutive bits to find the symbol being represented
        symbol = 0
        i = 0
        for bit in bits:
            symbol += bit << i
            i += 1
            if i >= bits_per_symbol:
                symbols.append(symbol)
                symbol = 0
                i = 0

        #print(''.join(map(str, symbols)))

        wave = np.concatenate(tuple(self.waves[symbol]for symbol in symbols))
        self.stop()
        sd.play(wave, samplerate=self.p.sample_rate, blocking=blocking)

    def stop(self) -> None:
        """ Stops any current modulation """
        sd.stop()


class Demodulator:
    def __init__(self, properties: SoundProperties, thresholds):
        if len(thresholds) != len(properties.frequencies):
            raise ValueError('Number of thresholds must match the number of frequencies')
        self.__properties = properties
        self.__thresholds = thresholds
        self.__thread = threading.Thread()
        self.__stream = sd.InputStream(
            samplerate=self.__properties.sample_rate,
            blocksize=self.__properties.block_size,
            channels=1,
        )

    def get_fft_frequencies(self):
        return np.fft.fftfreq(self.__properties.block_size, 1 / self.__properties.sample_rate)[:self.__properties.block_size // 2]

    def demodulate(self, buffer: Queue, blocking: bool=False):
        if not blocking:
            self.__thread = threading.Thread(target=self.demodulate, args=(buffer, True))
            self.__thread.start()
            return
        
        freq_indexes = tuple(np.where(np.isclose(self.get_fft_frequencies(), freq))[0][0] for freq in self.__properties.frequencies)

        print('Freq indexes:', freq_indexes)
        print(' '.join(map(str, (freq for freq in self.get_fft_frequencies() if freq < 20000))))
        #tuple(self.__closest_frequency_index(self.__properties.block_size, self.__properties.sample_rate, freq) for freq in self.__properties.frequencies)

        subsymbol = -1
        count = 0

        with self.__stream as stream:
            while self.__stream.active:
                try:
                    block = stream.read(self.__properties.block_size)[0]
                except sd.PortAudioError:
                    break
                magnitudes = abs(np.fft.rfft(block[:, 0])[:self.__properties.block_size // 2])

                max_delta = 0
                max_freq_index = -1

                # finding the frequency based on the difference between each frequency's 
                # magnitude and its threshold
                for i in range(len(self.__properties.frequencies)):
                    delta = magnitudes[freq_indexes[i]] - self.__thresholds[i]
                    if delta > max_delta:
                        max_delta = delta
                        max_freq_index = i

                # at this point `max_freq_index` is equal to the symbol

                #if max_freq_index != -1:
                    #print(list(magnitudes))
                    #print(' '.join(str(round(magnitudes[freq_indexes[i]], 2)).ljust(4, '0').rjust(6, ' ') for i in range(len(freq_indexes))), flush=True)

                if count > 0 and max_freq_index != subsymbol:
                    count = round(count / self.__properties.blocks_per_symbol)
                    #print(str(subsymbol) * count, end='', flush=True)
                    for _ in range(count):
                        buffer.put(subsymbol)
                    count = 0
                subsymbol = max_freq_index
                count += 1

    def stop(self):
        self.__stream.abort()
        try:
            self.__thread.join()
        except RuntimeError:
            pass