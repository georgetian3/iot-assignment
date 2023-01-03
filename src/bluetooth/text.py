from .bluetooth import BluetoothSender, BluetoothReceiver
import threading
from bitarray import bitarray
import queue

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
        self.__bits = bitarray()
        self.__thread = threading.Thread()
        self.__text = ''
        
    def decode(self, blocking: bool=False):
        if not blocking:
            self.__thread = threading.Thread(target=self.decode, args=(True,), daemon=True)
            self.__thread.start()
            return

        self.__bits = bitarray()
        self.__text = ''

        bits_buffer = queue.Queue()
        self.__receiver.receive(bits_buffer)

        self.__running = True
        while self.__running:
            try:
                bit = bits_buffer.get(timeout=0.1)
                if bit == None:
                    #print('got none')
                    return
                self.__bits.append(bit)
            except queue.Empty:
                continue

    def get(self):
        try:
            self.__text = self.__bits.tobytes().decode(self.__encoding)
        except UnicodeDecodeError:
            pass
        return self.__text

    def running(self):
        try:
            self.__thread.join(0)
            return self.__thread and self.__thread.is_alive()
        except RuntimeError:
            return False

    def stop(self):
        self.__running = False
        try:
            self.__thread.join()
        except RuntimeError:
            pass
        self.__receiver.stop()