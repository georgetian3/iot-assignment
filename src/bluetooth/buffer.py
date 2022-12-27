from queue import Queue

class BufferStoppedError(Exception):
    def __init__(self):
        super().__init__('Error: buffer has stopped')


def buffer_get_bit(buffer: Queue) -> int:
    #print('waiting buffer')
    bit = buffer.get()
    #print('got buffer')
    if bit == None:
        raise BufferStoppedError
    return bit