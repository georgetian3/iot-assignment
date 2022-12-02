from matplotlib import pyplot as plt
from numpy import pi
import numpy as np


def graph(x, y, x_label: str='', y_label: str='', title=''):
    plt.plot(x, y, linewidth=0.5, color='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()


def sine_wave(
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