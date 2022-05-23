import pexpect


def demo():
    output = pexpect.run('df -h').decode('utf-8')
    child = pexpect.spawn('df -h')
    ret = child.expect(pexpect.EOF)
    out1 = child.before.decode('utf-8')

    print('done demo')


if __name__ == '__main__':
    demo()