from multiprocessing.pool import ThreadPool
import time


def wrapper(args):
    print(*args)
    foo(*args)


def foo(name, age):
    if name == 'fancy':
        time.sleep(1)
    print(f'hi {name}, you are {age}')


def multi_thread_pool():
    name = ['fancy', 'sof', 'jenny', 'jerry']
    age = [41, 40, 11, 4]
    pool = ThreadPool(10)
    # launch thread
    # for i in range(4):
    #     pool.apply_async(foo, args=(name[i], age[i]))
    # another way to launch thread, passing more than 1 arg
    pool.map(wrapper, zip(name, age))
    pool.close()
    pool.join()


if __name__ == '__main__':
    multi_thread_pool()
