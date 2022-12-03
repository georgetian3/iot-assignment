from .soundproperties import SoundProperties

import numpy as np
from threading import Thread
import sounddevice as sd

class Modulator:
    def __init__(self, properties: SoundProperties):
        """
        `properties`: physical properties of the sound wave to be modulated and transmitted
        """
        self.p = properties
        self.waves = tuple(
            np.sin(
                2 * np.pi * freq *
                np.arange(round(self.p.sample_rate * self.p.symbol_duration))
                / self.p.sample_rate
            ) for freq in (self.p.f0, self.p.f1)
        )
    
    def modulate(self, bits: str) -> np.ndarray:
        """
        `bits`: string of 0s and 1s
        Returns: sound wave of `bits`
        """
        if not set(bits).issubset(set('01')):
            raise ValueError('bits must only contain 0s and 1s')
            
        wave = np.concatenate(tuple(self.waves[int(bit)] for bit in bits))

        return wave

    def play(self, wave, blocking=False):
        if not blocking:
            Thread(target=self.play, args=(wave, True), daemon=True).start()
            return
        sd.play(wave, samplerate=self.p.sample_rate)

    def stop(self):
        sd.stop()