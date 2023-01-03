from app.app import app
from bluetooth.main import buffer, modulator, demodulator, sender, receiver, encoder, decoder, print_queue
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-bs', help='Run Bluetooth sender, argument is the text to be send')
    parser.add_argument('-br', action='store_true', help='Run Bluetooth receiver')
    parser.add_argument('-ds', action='store_true', help='Run distance sender')
    parser.add_argument('-dr', help='Run distance receiver, argument is IP address of sender')
    parser.add_argument('--gui', action='store_true', help='Run GUI')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.bs:
        encoder.encode(args.s)
        input('Press enter to stop...')
    elif args.br:
        decoder.decode()
        while decoder.running():
            print(decoder.get(), end='\r')
            time.sleep(0.1)
        print(decoder.get())
    elif args.ds:
        pass
    elif args.dr:
        pass
    elif args.gui:
        port = 8000
        print(f'Visit http://localhost:{port}')
        app.run(debug=False, port=port)
    

if __name__ == '__main__':
    main()