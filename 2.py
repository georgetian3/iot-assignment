# reading audio files
from typing import Iterable
from pydub import AudioSegment

import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from matplotlib.pyplot import specgram

import random


def graph(x, y, x_label: str='', y_label: str='', title=''):
    plt.plot(x, y, linewidth=0.5, color='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()

def spectrogram(samples: list, sample_rate: float, nttf: int, title: str='') -> None:
    """
    Graphs a time-frequency-magnitude spectrogram using matplotlib's `specgram`

    Parameters:
        `samples`: raw sample points
        `sample_rate`: Hz
        `nttf`: window size
        `title`: title of the graph

    Returns: `None`
    """
    specgram(samples, nttf, sample_rate)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.plot()
    plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()

def graph_freq_amp(samples, sample_rate=48000, title='') -> None:
    """
    Graphs a frequency-magnitude spectrogram

    Parameters:
        `samples`: raw sample points
        `sample_rate`: Hz
        `title`: title of the graph

    Returns: `None`
    """
    freqs, amps = dft_to_freq_amp(dft(samples), sample_rate)
    graph(freqs, amps, 'Frequency', 'Magnitude', title)


def a(N):
    return [1] * N

def b(N):
    return [1 - n / N for n in range(N)]

def c(N):
    return [np.sin(2 * pi * n / N) for n in range(N)]

def extend(samples: Iterable) -> None:
    """
    Returns `samples` extended using 0s to 10x its original length
    Does not modify `samples
    """
    return samples + [0] * len(samples) * 9

def read():
    """
    Reads `res.wav` and returns its sample points and sample rate
    """
    signal = AudioSegment.from_file('res.wav')
    return list(signal.get_array_of_samples()), signal.frame_rate

def dft(x: Iterable) -> list:
    """
    Performs discrete Fourier transform on `x`

    Parameters:
        `x`: contains each sample point

    Returns: list of same size as `x`, where the `i`th item is the `i`th coefficient
    """
    N = len(x)
    X = [0] * N
    for k in range(N // 2):
        c = -2j * pi * k / N
        X[k] = sum(x[n] * np.exp(c * n) for n in range(N))

    return X

def test_dft() -> None:
    """
    Compares my implementation of DFt against numpy's fft
    """
    len = 100
    repeats = 100
    delta = 1e-10

    for _ in range(repeats):
        x = [random.random() for _ in range(len)]
        a = dft(x)
        b = np.fft.fft(x)
        for i in range(len):
            if abs(a[i] - b[i]) > delta:
                print('DFT test failed')
                return
    print('DFT test succeeded')

def dft_to_freq_amp(dft: Iterable, sample_rate: float) -> list:
    """
    Converts DFT coefficients into frequencies and their corresponding magnitudes

    Parameters:
        `dft`: DFT coefficients
        `sample_rate`: Hz

    Returns `(freqs, amps)`, both of which are lists, where the `i`th item
    in `amps` is the amplitude of the frequency in `freqs[i]`
    """

    N = len(dft)
    c = sample_rate / N
    freqs = [i * c for i in range(N)]
    amps = [abs(dft[i]) / c for i in range(N)]
    return freqs, amps





def run():
    """
    Runs all the required tests
    """

    # graphs the functions a, b, c
    # defaulting to sample_rate=48000Hz
    for f in [a, b, c]:
        for N in [32, 128, 1024]:
            graph_freq_amp(f(N), title=f'function:{f.__name__}, N = {N}')

    samples, sample_rate = read()
    # graph `res.wav` with no padding
    graph_freq_amp(samples, sample_rate, 'res.wav, no padding')

    extended_samples = extend(samples)
    # graph `res.wav` with padding
    graph_freq_amp(extended_samples, sample_rate, 'res.wav, 10x padding')

    # graph `res.wav` with different padding
    Ns = [200, 300, 400, 500, 600, 700, 800, 900, 1000]
    for N in Ns:
        spectrogram(samples, sample_rate, N, f'res.wav, N = {N}')

if __name__ == '__main__':
    run()
