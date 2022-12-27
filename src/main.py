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

    texts = ['教材名称：Elementary probability theory,教材出版社:Springer,出版时间:2003,版次:fourth Edition,主要编者:Kai Lai Chung and Farid AitSahlia,主编单位:,评价:很合适;', '1．Kai Lai Chung and Farid AitSahlia，Elementary probability theory, Springer, 2003, fourth Edition.（英文） 2．M. Spiegel，J. Schiller and R. Srinivasan, Probability and Statistics. (英文)', 'Open Office Hour成绩评定标准教师教学特色中文授课、英文教']

    text = texts[0]
    from queue import Queue, Empty
    buffer = Queue()

    #data = [1 if x == '1' else 0 for x in '1010101000000000001000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111010101010000000001000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111010101001000000001000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111010101011000000001000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111010101000100000001000001111010111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111']
    #data = [1, 0, 1] * 100
    #print(''.join(map(str, data)))
    #print(text)

    #for text in texts:
    #print(''.join(map(str, data)))

    """ ba = bitarray()
    ba.frombytes(text.encode('utf8'))
    print(ba.to01())
    data = list(ba) """

    if args.test_bluetooth_sender:
        
        #modulator.modulate(data)
        
        #sender.send(ba)
        encoder.encode(text, blocking=True)
        input()
    elif args.test_bluetooth_receiver:
        #demodulator.demodulate(buffer)
        #receiver.receive(buffer)
        decoder.decode(blocking=True)

    #input()
    if args.test_bluetooth_receiver:
        """ receiver.stop()
        #demodulator.stop()
        received = []
        while not buffer.empty():
            received.append(buffer.get())
        if received[-1] == None:
            received.pop()
        print(len(received))
        print(received == data)
        print(bitarray(received).tobytes().decode('utf8')) """
        try:
            while decoder.running():
                #print(decoder.get())
                sleep(0.2)
            print('DONE')
            print(decoder.get())
        except KeyboardInterrupt:
            decoder.stop()








    return
    if args.gui:
        print('Running GUI')
        app.run(debug=False, port=8000)
    elif args.test_bluetooth_sender:
        print('Running Bluetooth sender test')
        tester = bluetooth.test.Tester(sender=sender)
        tester.run()
    elif args.test_bluetooth_receiver:
        print('Running Bluetooth receiver test')
        tester = bluetooth.test.Tester(receiver=receiver)
        tester.run()
    elif args.test_distance_sender:
        print('Running distance sender test')
        pass
    elif args.test_distance_receiver:
        print('Running distance receiver test')

if __name__ == '__main__':
    main()
