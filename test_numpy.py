import numpy as np


def demo1():
    # basic
    a = np.array([[1, 2, 3, 4, 5],
                  [6, 7, 8, 9, 10]], dtype='int16')
    dim = a.ndim
    shape = a.shape
    dtype = a.dtype
    itemsize = a.itemsize
    total_size = a.nbytes

    # accessing/changing specific elements, rows, columns, etc;
    ele2_3 = a[1, -1]
    row1 = a[0, :]
    col1 = a[:, 1]
    # [startindex:endindex:stepsize]

    a[:, 1] = [10, 20]
    print(a)


if __name__ == '__main__':
    demo1()
