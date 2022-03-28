import os


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def demo():
    try:
        os.mkdir('/home/fanxin/tmp')
    except Exception as e:
        pass
    os.chdir('/home/test/cudnn_pkg')
    div = ['a', 'b', 'c', 'd']
    for i, ele in enumerate(div):
        print(ele, i)

    # list all env variables
    for k, v in sorted(os.environ.items()):
        print(k + ':', v)


def demo1():
    cmd = "axel %s -o %s -p" % ('url_dw', 'f')
    cmd1 = "axel {c1} -o {c2} -p".format(c1='aa', c2='dd')

    cwd = os.getcwd()
    os.chdir('/home')
    os.chdir(cwd)
    print(cmd1)

    files = os.listdir()
    pkgs = []
    for file in files:
        if file.endswith('tgz'):
           pkgs.append(file)
    pkgs.remove('SW_31121986.0_cudnn_dev_gpgpu_cuda_a_Release_Linux_Ubuntu20_04_AMD64_CUDNN_TESTS.tgz')
    for pkg in pkgs:
        os.remove(pkg)
    print(pkgs)


def demo_class():
    p = Person('fancy', 40)
    print(p.name, p.age)


def demo_file_op():
    with open('tmp.txt', 'r') as f:
        for each in f:
            print(each)


if __name__ == '__main__':
    demo()
    demo1()
    demo_class()
    # demo_file_op()
