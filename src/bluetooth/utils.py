""" from matplotlib import pyplot as plt
import numpy as np

def graph(x, y=None, x_label: str='', y_label: str='', title='', save=False):
    if type(y) != np.ndarray and y == None:
        y = x
        x = list(range(len(x)))
    plt.plot(x, y, linewidth=0.5, color='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if save:
        plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()


 """


def get_bit(bytes, i):
    byte = bytes[i // 8]
    bit = (byte >> (7 - i % 8)) & 1
    return bit

def str_to_bit(s: str, encoding='ascii') -> str:
    s = bytes(s, encoding)
    bits = [get_bit(s, i) for i in range(len(s) * 8)]
    return ''.join(map(str, bits))