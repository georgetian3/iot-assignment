from .bluetooth import BluetoothSender, BluetoothReceiver
from .soundproperties import SoundProperties
from .modem import Modulator, Demodulator
from .text import TextEncoder, TextDecoder
import queue
import numpy as np
import time

properties = SoundProperties(
    frequencies=[9000, 12000],
    sample_rate=384000,
    block_size=2 ** 11,
    blocks_per_symbol=8,
)

""" bitrate = properties.sample_rate / (properties.block_size * properties.blocks_per_symbol) * int(np.log2(len(properties.frequencies)))
print('Bitrate:', bitrate, 'symbols/second')
waves_per_symbol = np.array(properties.frequencies) / bitrate
print('Waves per symbol:', waves_per_symbol)
waves_per_block = waves_per_symbol / properties.blocks_per_symbol
print('Waves per block:', waves_per_block) """


buffer = queue.Queue()

modulator = Modulator(properties)
demodulator = Demodulator(properties, thresholds=[10, 10])
sender = BluetoothSender(modulator)
receiver = BluetoothReceiver(demodulator)
encoder = TextEncoder(sender)
decoder = TextDecoder(receiver)
