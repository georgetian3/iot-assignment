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