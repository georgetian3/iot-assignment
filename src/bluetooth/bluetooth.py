from typing import Iterable
from .bluetoothpacket import BluetoothPacket

from modem.modulator import Modulator
from modem.demodulator import Demodulator
from . import utils

from queue import Queue
import threading

import sys

class BluetoothSender:
    def __init__(self, modulator: Modulator):
        self.__modulator = modulator

    def __serialize(self, text: str) -> Iterable:

        data = text.encode('ascii')
        if len(data) >= 2 ** 32:
            # only support sizeof(int) length
            raise ValueError('Text too long')
        preamble = [1, 0, 1, 0, 1, 0, 1, 0]

        payload_length = list(map(int, bin(len(data))[2:].rjust(32, '0')[::-1]))

        print('Payload length:', payload_length)

        payload = [utils.get_bit(data, i) for i in range(len(data) * 8)]

        print('Payload:', payload)


        return preamble + payload_length + payload


    def send(self, text: str, blocking=False) -> None:

        """
        Text: ASCII string
        """

        data = self.__serialize(text)

        wave = self.__modulator.modulate(data)
        self.__modulator.play(wave, blocking)

        return data


class BluetoothReceiver:
    def __init__(self, demodulator: Demodulator):
        self.__demodulator = demodulator


    def receive(self, text_buffer: Queue, blocking=False) -> BluetoothPacket:
        if not blocking:
            threading.Thread(target=self.receive, args=(text_buffer, True), daemon=True).start()
            return

        self.__stop = False
        buffer = Queue(1024)
        self.__demodulator.demodulate(buffer)
        while not self.__stop:
            invalid_bit = False

            bit = buffer.get()
            if bit == -1:
                continue
                print(' ', end='')
            else:
                print(bit, end='')
            sys.stdin.flush()
            continue

            # find preamble
            preamble = 0
            while not self.__stop and preamble != 0b10101010:
                bit = buffer.get()
                if bit == -1: # reset on invalid bit
                    print('X1')
                    preamble = 0
                else:
                    preamble = ((preamble << 1) & 0b11111111) + bit
            print('Found preamble')

            # find 32 bit packet length
            payload_length = 0
            for _ in range(32):
                bit = buffer.get()
                if bit == -1:
                    print('X2')
                    invalid_bit = True
                    break
                payload_length = (payload_length << 1) + bit

            if invalid_bit: # reset on invalid bit
                continue
            print('Payload length:', payload_length)
            for _ in range(payload_length):
                byte = 0
                for _ in range(8):
                    bit = buffer.get()
                    if bit == -1:
                        print('X3', end='')
                        sys.stdin.flush()
                        text_buffer.put(-1)
                        invalid_bit = True
                        break
                    byte = (byte << 1) + bit
                if invalid_bit:
                    break
                print('Found byte:', chr(byte))
                text_buffer.put(chr(byte))

            if invalid_bit:
                continue

            text_buffer.put(0) # null byte
        self.__demodulator.stop()

    def stop(self):
        self.__stop = True





