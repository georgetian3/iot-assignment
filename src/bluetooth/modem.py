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

        #print('Modulating:\n' + ''.join(map(str, symbols)))

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
            self.__thread = threading.Thread(target=self.demodulate, args=(buffer, True), daemon=True)
            self.__thread.start()
            return

        #print(list(self.get_fft_frequencies()))
        freq_indexes = tuple(np.where(np.isclose(self.get_fft_frequencies(), freq))[0][0] for freq in self.__properties.frequencies)


        prev_subsymbol = -1
        subsymbol = -1
        subsymbol_count = 0

        try:
            with self.__stream as stream:
                while stream.active:
                    block = self.__stream.read(self.__properties.block_size)[0]
                    magnitudes = abs(np.fft.rfft(block[:, 0])[:self.__properties.block_size // 2])

                    max_delta = 0
                    subsymbol = -1

                    # finding the frequency based on the difference between each frequency's 
                    # magnitude and its threshold
                    for i in range(len(self.__properties.frequencies)):
                        delta = magnitudes[freq_indexes[i]] - self.__thresholds[i]
                        if delta > max_delta:
                            max_delta = delta
                            subsymbol = i

                    #print(' '.join(str(round(magnitudes[freq_indexes[i]], 2)).ljust(4, '0').rjust(6, ' ') for i in range(len(freq_indexes))), flush=True)

                    if subsymbol != prev_subsymbol:
                        subsymbol_count = round(subsymbol_count / self.__properties.blocks_per_symbol)
                        for _ in range(subsymbol_count):
                            if prev_subsymbol != -1:
                                pass
                                #print(prev_subsymbol, end='', flush=True)
                            buffer.put(prev_subsymbol)
                        subsymbol_count = 1
                    prev_subsymbol = subsymbol
                    subsymbol_count += 1
                    
        except sd.PortAudioError:
            pass


    def stop(self):
        self.__stream.abort()
        try:
            self.__thread.join()
        except RuntimeError:
            pass