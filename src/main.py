import argparse
from app.app import app
from bluetooth.main import sender, receiver, modulator, demodulator, encoder, decoder
import bluetooth.test
import distance.test
import sys
from time import sleep
from bitarray import bitarray

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--gui', action='store_true')

    group.add_argument('--test_bluetooth_sender', action='store_true')
    group.add_argument('--test_distance_sender', action='store_true')

    group.add_argument('--test_bluetooth_receiver', action='store_true')
    group.add_argument('--test_distance_receiver', action='store_true')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if args.gui:
        print('Running GUI')
        app.run(debug=False, port=8000)
    elif args.test_bluetooth_sender:
        print('Running Bluetooth tests as sender')
        tester = bluetooth.test.Tester(sender=sender)
        tester.run()
    elif args.test_bluetooth_receiver:
        print('Running Bluetooth tests as receiver')
        tester = bluetooth.test.Tester(receiver=receiver)
        tester.run()
    elif args.test_distance_sender:
        print('Running distance sender test')
        pass
    elif args.test_distance_receiver:
        print('Running distance receiver test')

if __name__ == '__main__':
    main()
