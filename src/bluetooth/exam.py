from queue import Queue
from typing import Iterable
import numpy as np
import sounddevice as sd
from .soundproperties import SoundProperties
from bitarray import bitarray

properties = SoundProperties(
    frequencies=[12000, 15000],
    sample_rate=384000,
    block_size=2 ** 7,
    blocks_per_symbol=8,
)


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

        #print('Modulating:')
        print(''.join(map(str, symbols)))

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
        self.__stream = sd.InputStream(
            samplerate=self.__properties.sample_rate,
            blocksize=self.__properties.block_size,
            channels=1,
        )

    def get_fft_frequencies(self):
        return np.fft.fftfreq(self.__properties.block_size, 1 / self.__properties.sample_rate)[:self.__properties.block_size // 2]

    def demodulate(self):
        bits = []
        freq_indexes = tuple(np.where(np.isclose(self.get_fft_frequencies(), freq))[0][0] for freq in self.__properties.frequencies)


        subsymbol = -1
        count = 0

        found_nonneg = False

        with self.__stream as stream:
            while True:
                block = stream.read(self.__properties.block_size)[0]

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

                if count > 0 and max_freq_index != subsymbol:
                    count = round(count / self.__properties.blocks_per_symbol)
                    if subsymbol != -1:
                        print(str(subsymbol) * count, end='', flush=True)
                        found_nonneg = True
                        bits.extend([subsymbol] * count)
                    elif found_nonneg and count >= self.__properties.blocks_per_symbol / 2: 
                        print('found nonneg')
                        return bits
                    count = 0
                subsymbol = max_freq_index
                count += 1

def exam_sender():
    s = input('Input string: ')
    m = Modulator(properties)
    #encoder.encode(s, blocking=True)
    ba = bitarray()
    ba.frombytes(s.encode('ascii'))
    m.modulate(ba, blocking=True)

    #sender.send(ba, blocking=True)

def exam_receiver():
    d = Demodulator(properties, thresholds=[1.8, 1.4])
    bits = d.demodulate()
    ba = bitarray(bits)
    print(ba.tobytes().decode('ascii'))
    return
    while True:
        bit = buffer.get()
        if bit != -1:
            break

    bits = bitarray()
    while True:
        bit = buffer.get()
        if bit == -1:
            break
        bits.append(bit)

    print('String:', bits.tobytes().decode('ascii'))
    return
    #receiver.receive(buffer)
    input()
    print(list(buffer.queue))
    return
    bits = bitarray()
    while not buffer.empty():
        bit = buffer.get(0.1)
        if bit == None:
            break
        bits.append(bit)
        print(bits.tobytes().decode('ascii'))
    print(bits.tobytes().decode('ascii'))
    """ with open('通信_24_田正祺.txt', 'w+') as f:
        f.write(s + '\n') """
    