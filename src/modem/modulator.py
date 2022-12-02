from soundproperties import SoundProperties

import numpy as np
from threading import Thread
import sounddevice as sd

class Modulator:
    def __init__(self, properties: SoundProperties):
        """
        `properties`: physical properties of the sound wave to be modulated and transmitted
        """
        self.p = properties
        # np.int32 is required, otherwise the frequency generated is not correct???
        self.waves = tuple(
            (self.p.amplitude * np.iinfo(np.int32).max * np.sin(
                2 * np.pi * freq *
                np.arange(round(self.p.sample_rate * self.p.duration))
                / self.p.sample_rate 
                + self.p.phase
            )).astype(np.int32) for freq in (self.p.freq_0, self.p.freq_1)
        )
    
    def modulate(self, bits: str, play=True):
        """
        `bits`: string of 0s and 1s
        """
        if not set(bits).issubset(set('01')):
            raise ValueError('bits must only contain 0s and 1s')
        wave = np.concatenate(tuple(self.waves[int(bit)] for bit in bits))

        if play:
            Thread(target=sd.play, args=(wave,), daemon=True).start()

        return wave

    def stop(self):
        sd.stop()