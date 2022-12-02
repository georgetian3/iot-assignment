import numpy as np
from time import sleep, time
from threading import Thread
from queue import Queue

import sounddevice as sd
import sys

from utils import graph

from soundproperties import SoundProperties




class Demodulator:
    def __init__(self, properties: SoundProperties):
        """
        `properties`: physical properties of the sound wave to be received and demodulated
        """
        self.p = properties
        self.buffer = Queue(self.dp.sample_rate)

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # Fancy indexing with mapping creates a (necessary!) copy:
        self.buffer.put(indata[::])

    def demodulate(self, buffer: Queue):
        stream = sd.InputStream(
            samplerate=self.dp.sample_rate,
            blocksize=1024,
            callback=self.__buffer_audio
        )

