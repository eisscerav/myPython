from multiprocessing import Process
from multiprocessing.pool import ThreadPool as Pool
from faker import Faker
import random


def f(x, y):
    ret = ''
    fake = Faker()
    profile = fake.simple_profile()
    profile[x] = y
    ret += profile.get('name')
    ret += profile.get('mail')
    ret += profile.get('address')
    return profile

def wrapper_f(args):
    return f(*args)

if __name__ == '__main__':
    X = random.sample(range(1, 30), 20)
    Y = random.sample(range(1, 100), 20)
    # start 4 worker processes
    with Pool(processes=4) as pool:
        # print "[0, 1, 4,..., 81]"
        out = pool.map(wrapper_f, zip(X, Y))
        print('done main')