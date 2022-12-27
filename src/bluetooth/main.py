from .bluetooth import BluetoothSender, BluetoothReceiver
from .soundproperties import SoundProperties
from .modem import Modulator, Demodulator
from .text import TextEncoder, TextDecoder
from queue import Queue
import numpy as np

properties = SoundProperties(
    frequencies=[12000, 15000],
    block_size=2 ** 7,
    sample_rate=384000,
    blocks_per_symbol=4,
)

bitrate = properties.sample_rate / (properties.block_size * properties.blocks_per_symbol) * int(np.log2(len(properties.frequencies)))
print('Bitrate:', bitrate, 'symbols/second')
waves_per_symbol = np.array(properties.frequencies) / bitrate
print('Waves per symbol:', waves_per_symbol)
waves_per_block = waves_per_symbol / properties.blocks_per_symbol
print('Waves per block:', waves_per_block)


buffer = Queue()

modulator = Modulator(properties)
demodulator = Demodulator(properties, thresholds=[5, 2]) # 5, 0.4
sender = BluetoothSender(modulator)
receiver = BluetoothReceiver(demodulator)
encoder = TextEncoder(sender)
decoder = TextDecoder(receiver)