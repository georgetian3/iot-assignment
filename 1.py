# reading audio files
from pydub import AudioSegment

import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from matplotlib.pyplot import specgram



def graph(x, y, x_label: str='', y_label: str='', title=''):
    plt.plot(x, y, linewidth=0.5, color='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()


def sin_wave(
        amplitude: float,
        frequency: float,
        phase: float,
        sample_rate: float,
        duration: float) -> np.ndarray:
    """
    Generates a sine wave

    Parameters
    - `amplitude`  : m
    - `frequency`  : Hz
    - `phase`      : rad
    - `sample_rate`: Hz
    - `duration`   : s

    Returns: `ndarray` containing the sample points
    """
    return amplitude * np.sin(
            2 * pi * frequency *
            np.arange(int(sample_rate * duration)) / sample_rate 
            + phase
        )

# Hz
FREQ_LOW = 440
FREQ_HIGH = 880
SAMPLE_RATE = 48000
# s
SYMBOL_DURATION = 0.1

AMPLITUDE = 1
PREAMBLE_OCTETS = 1

PREAMBLE_BITS = '01' * 4 * PREAMBLE_OCTETS

sig = [
    sin_wave(AMPLITUDE, FREQ_LOW, 0, SAMPLE_RATE, SYMBOL_DURATION),
    sin_wave(AMPLITUDE, FREQ_HIGH, 0, SAMPLE_RATE, SYMBOL_DURATION)
]

def encode(bits: str):
    if not set(bits).issubset(set('01')):
        raise ValueError('bits must only contain 0 and 1')

    wave = np.array()
    for bit in bits:
        wave = wave.append(wave, sig[int(bit)])
    return wave

def run():
    pass

if __name__ == '__main__':
    print(PREAMBLE_BITS)
