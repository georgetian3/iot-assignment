import numpy as np
from time import sleep
from threading import Thread
from queue import Queue

from sounddevice import InputStream, play
import sys

class SignalProperties:
    def __init__(self, 
        amplitude: float,
        freq_0: float,
        freq_1: float,
        phase: float,
        sample_rate: int,
        duration: float
    ):

        if freq_0 < 0 or freq_1 < 0:
            raise ValueError('Frequency cannot be negative')
        if sample_rate < 0:
            raise ValueError('Frequency cannot be negative')
        if duration < 0:
            raise ValueError('Frequency cannot be negative')

        self.amplitude = amplitude
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self.phase = phase
        self.sample_rate = sample_rate
        self.duration = duration




class Modem:
    def __init__(self,
        modulating_properties: SignalProperties,
        demoduating_properties: SignalProperties
    ):
        self.mp = modulating_properties
        self.dp = demoduating_properties

        self.waves = tuple(
            (self.mp.amplitude * np.sin(
                2 * np.pi * freq *
                np.arange(int(self.mp.sample_rate * self.mp.duration))
                / self.mp.sample_rate 
                + self.mp.phase
            )).astype(np.float32) for freq in (self.mp.freq_0, self.mp.freq_1)
        )

        self.buffer = Queue(self.dp.sample_rate)

    def modulate(self, bits: str):

        if not set(bits).issubset(set('01')):
            raise ValueError('bits must only contain 0s and 1s')

        signal = np.array([])

        for bit in bits:
            signal = np.append(signal, self.waves[int(bit)])

        print(signal)

        Thread(target=play, args=(signal,), daemon=True).start()


    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # Fancy indexing with mapping creates a (necessary!) copy:
        self.buffer.put(indata[::])

    def demodulate(self, buffer: Queue):
        stream = InputStream(
            samplerate=self.dp.sample_rate,
            blocksize=1024,
            callback=self.__buffer_audio
        )

if __name__ == '__main__':
    p = SignalProperties(1, 440, 880, 0, 48000, 0.1)
    modem = Modem(p, p)

    bits = '01' * 100
    modem.modulate(bits)
    input('Press enter to continue...')