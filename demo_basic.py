import glob
import subprocess
import os
import re
import pandas as pd
import sys
import datetime
try:
    import django
except ModuleNotFoundError as e:
    python = sys.executable
    subprocess.run(f'{python} -m pip install django')


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


def demo():
    str_ = '高 手 大 人'
    s = str_.replace(r' ', '')
    try:
        os.mkdir('/home/fanxin/tmp')
    except Exception as e:
        pass
    div = ['a', 'b', 'c', 'd']
    for i, ele in enumerate(div):
        print(ele, i)

    # list all env variables
    for k, v in sorted(os.environ.items()):
        print(k + ':', v)

    def is_odd(n):
        return n % 2 == 1
    odd = list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
    odd_ = list(filter(lambda x: x % 2 == 1, [1, 2, 4, 5, 6, 9, 10, 15]))
    from functools import reduce
    li = [11, 22, 33]
    result = reduce(lambda a, b: a + b, li)
    li = [11, 22, 33]
    sl = [1, 2, 3]
    new_list = map(lambda a, b: a + b, li, sl)

    l1 = list(map(lambda x: x.capitalize(), ['adam', 'LISA', 'barT']))
    print('demo')


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
    # read from a file
    # with open('tmp.txt', 'r') as f:
    #     for each in f:
    #         print(each)
    # write to a file
    try:
        os.mkdir('tmp')
    except Exception as e:
        print(e)
    with open('tmp/tmp1.txt', 'w') as fp:
        fp.write('fanny')
        fp.write('philip')


def parse_offline_program():
    root = r'D:\VM_shared'
    my = open(os.path.join(root, 'my.txt'), 'r')
    other = open(os.path.join(root, 'other.txt'), 'r')

    my_list = []
    other_list = []
    for each in my:
        my_list.append(each.replace(' ', '').strip())
    for each in other:
        other_list.append(each.replace(' ', '').strip())

    for each_other in other_list:
        if each_other in my_list:
            print('{}\tyes'.format(each_other.strip()))
        else:
            print('{}\tno'.format(each_other.strip()))


def demo_chinese():
    p = re.compile(r'\(.*\)')
    a = ['高手', '低手', 'aaa ed (快手)']
    o = a[-1]
    t = p.sub('', o)
    if '快' in a:
        print('yes')

def foo(*args):
    for arg in args:
        print(arg)

def bar(**kargs):
    for k in kargs:
        print(f'{k}: {kargs[k]}')


def demo_datetime():
    date = datetime.date(2020, 5, 17)  # create date
    date_v2 = datetime.datetime.strptime('2021-10-22', '%Y-%m-%d').date()  # convert string to date
    print('done demo_datetime')


def main():
    l = ['arch80', 'host']
    s = '_'.join(l)
    my_dict = {
        'name': 'fan',
        'age': 20
    }
    for k, v in my_dict.items():
        print(k, v)
    import shutil
    cmd = shutil.which('gcc')
    y = [x for x in range(10)]
    foo(*y)
    my_data = dict()
    for e in y:
        my_data[f'{e}'] = e**2
    bar(**my_data)
    print(pow(2, 3))
    l1 = [1, 2, 3]
    l2 = [4, 5]
    l3 = zip(l1, l2)
    for l in l3:
        print(l)
    env = ''
    with open('env.txt', 'w') as fp:
        for k in os.environ:
           str_ = f'{k}={os.environ[k]}\n'
           env += str_
           # print(str_)
        fp.writelines(env)
    # demo()
    # demo1()
    # demo_class()
    # demo_file_op()
    # parse_offline_program()
    # demo_chinese()
    print('done main')


if __name__ == '__main__':
    main()
