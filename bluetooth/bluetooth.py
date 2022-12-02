from bluetoothpacket import BluetoothPacket


from .utils import sine_wave
import numpy as np





class Bluetooth:
    def __init__(self, freq_high, freq_low, sample_rate, bit_duration, amplitude):
        self.__freq_high = freq_high
        self.__freq_low = freq_low
        self.__sample_rate = sample_rate
        self.__bit_duration = bit_duration
        self.__amplitude = amplitude


class BluetoothSender(Bluetooth):
    def __init__(self, freq_high, freq_low, sample_rate, bit_duration, amplitude):
        super().__init__(freq_high, freq_low, sample_rate, bit_duration, amplitude)
        self.__sig = [
            sine_wave(amplitude, freq, 0, sample_rate, bit_duration)
                for freq in (freq_low, freq_high)
        ]

    def encode(self, bits: str) -> BluetoothPacket:
        if not set(bits).issubset(set('01')):
            raise ValueError('bits must only contain 0 and 1')

        wave = np.array()
        for bit in bits:
            wave = wave.append(wave, self.__sig[int(bit)])
        return wave

    def send(self, packet: BluetoothPacket) -> None:
        pass

class BluetoothReceiver(Bluetooth):
    def __init__(self, freq_high, freq_low, sample_rate, bit_duration, amplitude):
        super().__init__(freq_high, freq_low, sample_rate, bit_duration, amplitude)


    def decode(self, packet: BluetoothPacket) -> str:
        pass

    def receive(self) -> BluetoothPacket:
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
