from matplotlib import pyplot as plt


def graph(x, y, x_label: str='', y_label: str='', title=''):
    plt.plot(x, y, linewidth=0.5, color='black')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(title + '.pgf')
    plt.show()
    plt.clf()


