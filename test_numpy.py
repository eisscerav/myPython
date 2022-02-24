import numpy as np
from setuptools import sic


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

    # initializing different types of arrays
    a1 = np.zeros((3, 4))
    a2 = np.ones((3, 4, 5), dtype='int16')
    a3 = np.full((2, 3), 99)
    # np.full(a1.shape, 88)
    a4 = np.full_like(a1, 88, dtype='int')
    a5 = np.random.rand(5, 4, 3)
    a6 = np.random.sample(a1.shape)
    a7 = np.random.randint(0, 10, size=(3, 3))
    a8 = np.identity(5)

    # deep copy for arrays
    b = a1.copy()

    # op on array
    c1 = a1 + 2
    c2 = a5 ** 2
    c3 = np.sin(a5)

    # Linear algebra
    d1 = np.random.randint(10, size=(2, 3))
    d2 = np.random.randint(10, size=(3, 2))
    d3 = np.matmul(d1, d2)
    # np.linalg.det(d3)

    # statistics
    print(a)


if __name__ == '__main__':
    demo1()
