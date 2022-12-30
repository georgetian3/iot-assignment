import argparse
from app.app import app
from bluetooth.main import properties, modulator, demodulator, buffer, exam_sender, exam_receiver
import bluetooth.test
import distance.test




parser = argparse.ArgumentParser()
def parse_args():
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--gui', action='store_true', help='Run GUI')

    group.add_argument('-d', action='store_true', help='Test Bluetooth as demodulator')
    group.add_argument('-m', action='store_true', help='Test Bluetooth as modulator')

    group.add_argument('-s', action='store_true', help='Test distance as sender')
    group.add_argument('-r', action='store_true', help='Test distance as receiver')

    group.add_argument('-es', action='store_true')
    group.add_argument('-er', action='store_true')

    parser.add_argument('-t', action='store_true')

    args = parser.parse_args()
    return args

def main():

    #bluetooth.test.gen_rand_bits(1000)
    from bitarray import bitarray
    ba = bitarray('010011000111' * 20)
    #ba = bitarray('10101010000000000000000011111010011000010111000001110011011001100110010101110000011011110110101001100110011100000110111100110011')
    args = parse_args()

    if args.gui:
        print('Running GUI')
        app.run(debug=False, port=8000)
    elif args.es:
        exam_sender()
    elif args.er:
        exam_receiver()
    elif args.m:
        if args.t:
            modulator.modulate(ba)
            input()
        else:
            bluetooth.test.run_modulator()
    elif args.d:
        if args.t:
            res = bitarray()
            demodulator.demodulate(buffer)
            input()
            while not buffer.empty():
                bit = buffer.get()
                if bit not in (0, 1):
                    continue
                res.append(bit)
            print(ba == res)

        else:
            bluetooth.test.run_demodulator()
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
