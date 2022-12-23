from typing import Iterable
import numpy as np
import sounddevice as sd
from .soundproperties import SoundProperties
#from matplotlib import pyplot as plt

class Modulator:
    def __init__(self, properties: SoundProperties):
        self.p = properties
        self.waves = tuple(
            np.sin(
                2 * np.pi * freq *
                np.arange(round(
                    #self.p.sample_rate * self.p.symbol_duration
                    self.p.block_size * self.p.blocks_per_symbol
                ))
                / self.p.sample_rate
            ) for freq in (self.p.f0, self.p.f1)
        )
        """ plt.plot(self.waves[0])
        plt.show()
        exit() """

    def modulate(self, data: Iterable) -> np.ndarray:
        """
        data: Iterable where each element is a truthy or falsy value, representing 1 and 0 bits, respectively
        Returns: sound wave representing `data`
        """

        wave = np.concatenate(tuple(self.waves[int(bit)] for bit in data))
        return wave

    def play(self, wave, blocking=False):
        sd.play(wave, samplerate=self.p.sample_rate, blocking=blocking)

    def stop(self):
        sd.stop()