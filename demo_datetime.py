from datetime import datetime


def demo():
    now = datetime.now()
    microsecond = now.microsecond
    stamp = now.timestamp()
    print('done demo')


if __name__ == '__main__':
    demo()
