import os


def demo():
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

if __name__ == '__main__':
    demo1()
