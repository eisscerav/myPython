import os


def demo():
    div = ['a', 'b', 'c', 'd']
    for i, ele in enumerate(div):
        print(ele, i)

    # list all env variables
    for k, v in sorted(os.environ.items()):
        print(k+':', v)


if __name__ == '__main__':
    demo()
