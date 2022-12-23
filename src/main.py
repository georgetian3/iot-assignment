from modem.modulator import Modulator
from modem.demodulator import Demodulator
from modem.soundproperties import SoundProperties
from bluetooth.bluetooth import BluetoothSender, BluetoothReceiver
import bluetooth.utils as utils
from time import time, sleep
from queue import Queue
import threading
import sys
#from routes import app
import sounddevice as sd
import argparse
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-r', action='store_true')
    args = parser.parse_args()
    return args


def main():
    #app.run(debug=False, port=8000)

    #print(sd.query_devices())
    #print(sd.query_devices(1))

    #print(sd.query_devices(3))

    """ print(sd.check_output_settings(3, 1, samplerate=384000))
    print(sd.check_input_settings(1, 1, samplerate=384000))


    exit() """

    p = SoundProperties(
        f0=12000,
        f1=13000,
        sample_rate=384000,
        symbol_duration=0.05,
        block_size=2 ** 9,
        blocks_per_symbol=2 ** 4,
    )

    bitrate = p.sample_rate / (p.block_size * p.blocks_per_symbol)
    print('Bitrate:', bitrate, 'bits/second')

    args = parse_args()
    buffer = Queue()

    m = Modulator(p)
    d = Demodulator(p, th0=2, th1=2)


    data = [1, 0] * 40

    if args.r:
        d.demodulate(buffer)

    if args.s:
        m.play(m.modulate(data), blocking=True)

    

    if args.r:
        input()
        d.stop()
        while not buffer.empty():
            bit = buffer.get()
            if bit == -1:
                print(' ', end='')
            else:
                print(bit, end='')
            sys.stdin.flush()

    return


    """ sender = BluetoothSender(m)
    receiver = BluetoothReceiver(d)



    

    text = 'test'


    text_received = []

    if args.r:
        print('Receiving')
        receiver.receive(buffer)
        input()

    if args.s:
        print('Sending, bitrate:', )
        sender.send(text, blocking=True)

    if args.r:
        while not buffer.empty():
            bit = buffer.get(timeout=1)
            if bit == -1:
                bit = ' '
            print(bit, end='')
            sys.stdin.flush()
        receiver.stop() """


if __name__ == '__main__':
    main()