from bluetoothpacket import BluetoothPacket


from ..modem.utils import sine_wave
import numpy as np

from ..modem.soundproperties import SoundProperties
from ..modem.modulator import Modulator
from ..modem.demodulator import Demodulator

from queue import Queue



class BluetoothSender:
    def __init__(self, properties: SoundProperties):
        self.__modulator = Modulator(properties)


    def encode(self, bits: str) -> BluetoothPacket:
        if not set(bits).issubset(set('01')):
            raise ValueError('bits must only contain 0 and 1')

        wave = np.array()
        for bit in bits:
            wave = wave.append(wave, self.__sig[int(bit)])
        return wave

    def send(self, packet: BluetoothPacket) -> None:
        self.__modulator.modulate(packet.bits)

class BluetoothReceiver:
    def __init__(self, properties: SoundProperties):
        self.__demodulator = Demodulator(properties)


    def decode(self, packet: BluetoothPacket) -> str:
        pass

    def receive(self) -> BluetoothPacket:
        buffer = Queue(1024)
        self.__demodulator.demodulate(buffer, 8192, 10)
        while True:
            print
        pass






















PREAMBLE_OCTETS = 1

PREAMBLE_BITS = '01' * 4 * PREAMBLE_OCTETS





def run():
    pass

if __name__ == '__main__':
    # Hz
    FREQ_LOW = 440
    FREQ_HIGH = 880
    SAMPLE_RATE = 48000
    # s
    SYMBOL_DURATION = 0.1

    AMPLITUDE = 1


    bts = BluetoothSender(FREQ_HIGH, FREQ_LOW, SAMPLE_RATE, SYMBOL_DURATION, AMPLITUDE)
    btr = BluetoothReceiver(FREQ_HIGH, FREQ_LOW, SAMPLE_RATE, SYMBOL_DURATION, AMPLITUDE)

    print(PREAMBLE_BITS)
