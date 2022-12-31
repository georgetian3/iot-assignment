from .bluetooth import BluetoothSender, BluetoothReceiver
from .soundproperties import SoundProperties
from .modem import Modulator, Demodulator
from .text import TextEncoder, TextDecoder
from queue import Queue, Empty
import numpy as np
from bitarray import bitarray
import time

properties = SoundProperties(
    frequencies=[12000, 15000],
    sample_rate=384000,
    block_size=2 ** 7,
    blocks_per_symbol=8,
)

bitrate = properties.sample_rate / (properties.block_size * properties.blocks_per_symbol) * int(np.log2(len(properties.frequencies)))
print('Bitrate:', bitrate, 'symbols/second')
waves_per_symbol = np.array(properties.frequencies) / bitrate
#print('Waves per symbol:', waves_per_symbol)
waves_per_block = waves_per_symbol / properties.blocks_per_symbol
print('Waves per block:', waves_per_block)


buffer = Queue()

modulator = Modulator(properties)
demodulator = Demodulator(properties, thresholds=[1.8, 1.4])
sender = BluetoothSender(modulator)
receiver = BluetoothReceiver(demodulator)
encoder = TextEncoder(sender)
decoder = TextDecoder(receiver)

def exam_sender():
    s = input('Input string: ')
    #encoder.encode(s, blocking=True)
    ba = bitarray()
    ba.frombytes(s.encode('ascii'))
    modulator.modulate(ba, blocking=True)

    #sender.send(ba, blocking=True)

def exam_receiver():
    buffer = Queue()
    bits = demodulator.demodulate(buffer, blocking=True)
    print(bits)
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
    