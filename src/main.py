from app.app import app
from bluetooth.main import buffer, modulator, demodulator, sender, receiver, encoder, decoder, print_queue
from distance.sender import Sender
from distance.receiver import Receiver
import argparse
import time
import Levenshtein

parser = argparse.ArgumentParser()
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-bs', help='Run Bluetooth sender, argument is the text to be send')
    parser.add_argument('-br', action='store_true', help='Run Bluetooth receiver')
    parser.add_argument('-ds', action='store_true', help='Run distance sender')
    parser.add_argument('-dr', help='Run distance receiver, argument is IP address of sender')
    parser.add_argument('--gui', action='store_true', help='Run GUI')
    parser.add_argument('--test', metavar=('sent', 'received'), nargs=2, help='Calculates packet loss rate and error rate')
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
        sender = Sender(args.port,args.dAA,args.dBB)
        sender.main()
    elif args.dr:
        receiver = Receiver(args.host,args.port)
        receiver.main()
    elif args.gui:
        port = 8000
        print(f'Visit http://localhost:{port}')
        app.run(debug=False, port=port)
    elif args.test:
        sent, received = args.test
        packet_loss_rate = 1 - len(received) / len(sent)
        error_rate = 1 - Levenshtein.ratio(sent, received)
        print('Packet loss rate:', packet_loss_rate)
        print('Error rate:', error_rate)
    else:
        parser.print_help()
    

if __name__ == '__main__':
    main()