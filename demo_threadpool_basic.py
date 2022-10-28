import time
from multiprocessing import Process
from multiprocessing.pool import ThreadPool as Pool
from faker import Faker
import random
import threading

# how to use, add @synchronized before a function
def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func

def f(x, y, z):
    ret = ''
    fake = Faker()
    profile = fake.simple_profile()
    profile[x] = y + z
    ret += profile.get('name')
    ret += profile.get('mail')
    ret += profile.get('address')
    time.sleep(1)
    return profile

def wrapper_f(args):
    return f(*args)

if __name__ == '__main__':
    X = random.sample(range(1, 30), 20)
    Y = random.sample(range(1, 100), 20)
    Z = random.sample(range(100, 1000), 20)
    # start 4 worker processes
    with Pool(processes=4) as pool:
        # print "[0, 1, 4,..., 81]"
        out = pool.map(wrapper_f, zip(X, Y, Z))
        pool.close()
        pool.join()
        print('done main')