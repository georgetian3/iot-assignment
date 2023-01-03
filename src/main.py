from app.app import app
from bluetooth.main import buffer, modulator, demodulator, sender, receiver, encoder, decoder, print_queue
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s')
    parser.add_argument('-r', action='store_true')
    parser.add_argument('--gui', action='store_true')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.s:
        encoder.encode(args.s)
        input('Press enter to stop...')
    elif args.r:
        decoder.decode()
        while decoder.running():
            print(decoder.get(), end='\r')
            time.sleep(0.1)
        print(decoder.get())
    elif args.gui:
        port = 8000
        print(f'Visit http://localhost:{port}')
        app.run(debug=False, port=port)
    

if __name__ == '__main__':
    main()