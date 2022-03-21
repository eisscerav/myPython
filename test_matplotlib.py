import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def demo():
    # basic graph
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]
    plt.plot(x, y, label='2x', color='green', linewidth=3, marker='.', markersize=12, markeredgecolor='red',
             linestyle='--')
    # Line number 2
    x2 = np.arange(0, 4.5, 0.5)
    plt.plot(x2, x2**2)

    fontdict = {'fontsize': 40, 'fontname': 'Comic Sans MS'}
    plt.title('First plot', fontdict=fontdict)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    # adjust unit of x axis
    plt.xticks(x)
    plt.yticks(y)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    demo()
