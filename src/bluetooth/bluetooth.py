import math
from queue import Queue, Empty
import threading
from typing import Iterable
from bluetooth.modem import Modulator, Demodulator
from bitarray import bitarray
from bitarray.util import int2ba
import time


class BluetoothSender:
    def __init__(self, modulator: Modulator):
        self.__modulator = modulator

    def encapsulate(self, data: Iterable) -> bitarray:

        #return text
        if len(data) == 0:
            raise ValueError('No data')

        max_packet_count = 0x100
        max_payload_size = 0x100

        if len(data) > max_packet_count * max_payload_size:
            raise ValueError('Data too long')

        preamble = bitarray('10101010')
        packets = bitarray()
        packet_count = math.ceil(len(data) / max_payload_size)

        for i in range(packet_count):
            packets += preamble
            packets += int2ba(i, 8, endian='little')
            packets += int2ba(packet_count - 1, 8, endian='little')
            lower = i * max_payload_size
            upper = min((i + 1) * max_payload_size, len(data))
            packets += int2ba(upper - lower - 1, 8, endian='little')
            packets += data[lower : upper]
        return packets

    def send(self, bits: Iterable, blocking=False) -> None:
        self.stop()
        packets = self.encapsulate(bits)
        print('BluetoothSender sending:', packets.to01())
        self.__modulator.modulate(packets, blocking)

    def stop(self) -> None:
        self.__modulator.stop()


class BluetoothReceiver:
    def __init__(self, demodulator: Demodulator):
        self.__demodulator = demodulator
        self.__thread = threading.Thread()

    def receive(self, out_buffer: Queue, blocking: bool=False) -> None:
        if not blocking:
            self.__thread = threading.Thread(target=self.receive, args=(out_buffer, True))
            self.__thread.start()
            return

        print('receiver starting')

        in_buffer = Queue()
        self.__demodulator.demodulate(in_buffer)


        def get_bit():
            while True:
                try:
                    bit = in_buffer.get_nowait()
                    if bit == -1:
                        return 0
                    return bit

                except Empty:
                    time.sleep(0.1)


        
        def get_byte():
            byte = 0
            for i in range(8):
                byte += get_bit() << i
            return byte

        last_packet = False
        self.__running = True
        while self.__running and not last_packet:
            # find preamble
            preamble = 0
            while self.__running:
                bit = in_buffer.get()
                if bit == -1:
                    continue
                preamble = ((preamble << 1) & 0b11111111) + bit
                if preamble == 0b10101010:
                    #print('Found preamble')
                    break

            # find 8 bit packet sequence number
            packet_sequence_number = get_byte()
            #print('Sequence number:', packet_sequence_number)
            # find 8 bit packet count
            packet_count = get_byte()
            if packet_sequence_number >= packet_count:
                #print('last packet')
                last_packet = True
            #print('Packet count:', packet_count)
            # find 8 bit payload length
            payload_length = get_byte() + 1
            #print('Payload length:', payload_length)
            for i in range(payload_length):
                bit = get_bit()
                #print(i, end=' ', flush=True)
                out_buffer.put(bit)
            #print('Finished packet')
            #print(flush=True)
        self.__demodulator.stop()
        out_buffer.put(None)
        self.__running = False


    def stop(self):
        self.__running = False
        try:
            self.__thread.join()
        except RuntimeError:
            pass


