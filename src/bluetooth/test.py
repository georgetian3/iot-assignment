import numpy as np
import random
from queue import Queue, Empty
from .main import modulator, demodulator, bitrate
from bitarray import bitarray
import time
import Levenshtein

def add_random_noise(wave):
    noise = np.random.normal(0,1,100)
    wave += noise

def gen_rand_bits(n=128):
    ba = bitarray()
    for _ in range(n):
        ba.append(random.randint(0, 1))
    with open('tests.txt', 'w') as f:
        f.write(ba.to01())


def run_modulator(repeats=10):
    print('Testing as modulator')

    with open('tests.txt') as f:
        bits = bitarray(f.read())
    
    #bits = bitarray([1, 1, 1, 0] * 1000)
    print('Sending:', bits)
    for i in range(repeats):

        print(f'Trial {i + 1} / {repeats}: modulating...', end='', flush=True)
        modulator.modulate(bits, blocking=True)
        print('done. Press enter to continue', end='')
        input()
    print('All trials completed')



def run_demodulator(repeats=10):
    print('Testing as demodulator, ')
    with open('tests.txt') as f:
        correct = f.read().strip()
    print('Correct:', correct)
    for i in range(repeats):

        buffer = Queue()
        demodulated = ''
        print(f'Trial {i + 1}: demodulating, press ctrl + c to end current trial...', end='', flush=True)
        demodulator.demodulate(buffer)
        time.sleep(bitrate * (len(correct) * 1.5))
        demodulator.stop()
        while not buffer.empty():
            bit = buffer.get()
            if bit in (0, 1):
                demodulated += str(bit)
        packet_loss = 1 - len(demodulated) / len(correct)
        error_rate = 1 - Levenshtein.ratio(demodulated, correct)
        print(f'done: packet loss {packet_loss}, error rate {error_rate}')
    print('All trials completed')