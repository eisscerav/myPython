import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def demo():
    # basic graph
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]

    # resize graph
    plt.figure(figsize=(5, 5), dpi=100)
    plt.plot(x, y, label='2x', color='green', linewidth=3, marker='.', markersize=12, markeredgecolor='red',
             linestyle='--')
    # Line number 2
    x2 = np.arange(0, 4.5, 0.5)  # select interval we want to plot points at

    plt.plot(x2[:5], x2[:5]**2, label='x^2')  # plot part of graph
    plt.plot(x2[4:], x2[4:]**2, linestyle=':')  # plot remainder of graph

    fontdict = {'fontsize': 40, 'fontname': 'Comic Sans MS'}
    plt.title('First plot', fontdict=fontdict)  # add a title
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.xticks(x)  # adjust unit of x axis
    plt.yticks(y)
    plt.legend()
    plt.savefig('first_fig.png')  # save image
    plt.show()


def demo2():
    # bar chart
    labels = ['fancy', 'sof', 'jenny']
    values = [40, 33, 12]
    bars = plt.bar(labels, values)
    bars[0].set_hatch('/')
    bars[1].set_hatch('o')
    plt.show()


if __name__ == '__main__':
    demo()
    # demo2()
