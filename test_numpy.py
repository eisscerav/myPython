import numpy as np


def demo1():
    # basic
    aa = np.ndarray(shape=(2,3,4))
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
    a5 = np.random.rand(5, 10, 8)
    a5_ = a5[:2, 2:7, 1:5]
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
    det = np.linalg.det(d3)

    # statistics: axis=1 means row base
    min_ = np.min(a6, axis=1)
    sum_ = np.sum(a6)

    # reorganizing array
    c1 = np.array([[1,2,3,4,5,6], [7,8,9,10,11,12]])
    reshape = c1.reshape(6, 2)

    v1 = np.vstack([c1, c1])
    h1 = np.hstack([c1, c1])

    # misc
    filedata = np.genfromtxt('test.txt', delimiter=',').astype('int')

    # boolean masking and advanced indexing
    bool_array = filedata > 5
    ge5 = filedata[(filedata > 5) & (filedata < 9)]
    filt = ge5[[0, 1]]
    print(a)


if __name__ == '__main__':
    demo1()
