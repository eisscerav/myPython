import sys


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


def main():
    f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成
    for i in f:
        print(i)
    # while True:
    #     try:
    #         print(next(f), end=" ")
    #     except StopIteration:
    #         sys.exit()


if __name__ == '__main__':
    main()
