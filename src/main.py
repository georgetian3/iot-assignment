import argparse
from app.app import app
from bluetooth.main import properties
import bluetooth.test
import distance.test


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--gui', action='store_true', help='Run GUI')

    group.add_argument('-d', action='store_true', help='Test Bluetooth as demodulator')
    group.add_argument('-m', action='store_true', help='Test Bluetooth as modulator')

    group.add_argument('-s', action='store_true', help='Test distance as sender')
    group.add_argument('-r', action='store_true', help='Test distance as receiver')

    args = parser.parse_args()
    return args

def main():

    #bluetooth.test.gen_rand_bits(1000)

    args = parse_args()

    if args.gui:
        print('Running GUI')
        app.run(debug=False, port=8000)
    elif args.m:
        bluetooth.test.run_modulator()
    elif args.d:
        bluetooth.test.run_demodulator()
    elif args.test_distance_sender:
        print('Running distance sender test')
        pass
    elif args.test_distance_receiver:
        print('Running distance receiver test')

if __name__ == '__main__':
    main()
