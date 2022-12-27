from queue import Queue, Empty
from .bluetooth import BluetoothSender, BluetoothReceiver
import threading
from bitarray import bitarray
from multiprocessing import Queue

class TextEncoder:
    def __init__(self, sender: BluetoothSender, encoding='utf8'):
        self.__sender = sender
        self.__encoding = encoding
    def encode(self, text: str, blocking: bool=False):
        data = bitarray()
        data.frombytes(text.encode(self.__encoding))
        self.__sender.send(data, blocking)
    def stop(self):
        self.__sender.stop()
    
class TextDecoder:
    def __init__(self, receiver: BluetoothReceiver, encoding='utf8'):
        self.__receiver = receiver
        self.__encoding = encoding
        self.__running = False
        self.__thread = None
        self.__bits = bitarray()
        self.__text = ''
        
        
    def decode(self, blocking: bool=False):

        if self.running():
            raise ValueError('`decode` already started')
            
        if not blocking:
            
            self.__thread = threading.Thread(target=self.decode, args=(True,))
            self.__thread.start()
            return

        self.__bits = bitarray()
        self.__text = ''

        self.__running = True
        bits_buffer = Queue()
        self.__receiver.receive(bits_buffer)
        while self.__running:
            print('text decode waiting bit')
            try:
                bit = bits_buffer.get(timeout=0.1)
            except Empty:
                print('text decode  timed out')
                continue
            print('text decode got bit')
            if bit == None:
                print('received none bit')
                break
            else:
                self.__bits.append(bit)

    def get(self):
        print('getting text')
        try:
            self.__text = self.__bits.tobytes().decode(self.__encoding)
        except UnicodeDecodeError:
            pass
        return self.__text

    def running(self):
        return self.__thread and self.__thread.is_alive()

    def stop(self):
        self.__running = False
        if self.running():
            self.__thread.join()
        self.__receiver.stop()