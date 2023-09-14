from multiprocessing.pool import ThreadPool
# from multiprocessing import RLock
from concurrent.futures import ThreadPoolExecutor
import requests
import random
from demo_requests import timer_func
from bs4 import BeautifulSoup
from faker import Faker
import threading

# lock = RLock()
persons = []
lock = threading.Lock()

class Person:
    def __init__(self):
        self.name = ''
        self.birthday = 0

root_url = r'http://scdvstransfer.nvidia.com/dvsshare/vol2/'
cudnn_urls = [
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_dvsConfigCheck/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_wddm-x64_Display_Driver/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_wddm-x64_Display_Driver_Package_import_ausdvs/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_wddm2-x64_Display_Driver/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_wddm2-x64_Display_Driver_Package_import_ausdvs/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_cuda_11.4_Release_Windows_x86_CUDA_Driver/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_orin_cuda_11.4_Release_Linux_Ubuntu20_04_AMD64_CUDNN_FRONTEND_UNIT_TESTS/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_v8.2_orin_cuda_11.4_Release_Linux_Ubuntu20_04_AMD64_CUDNN_SAMPLES_TESTS/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/r10.1u2_GA_ossuary_Release_Windows_AMD64_GPGPU_CUDA_CUBLAS_CUDNN/',
    'http://scdvstransfer.nvidia.com/dvsshare/vol2/r10.2_GA_ossuary_Release_Windows_AMD64_GPGPU_CUDA_CUBLAS_CUDNN/',
]

# todo: demo thread lock(Thread Synchronization), refer to https://wrapt.readthedocs.io/en/latest/examples.html#thread-synchronization
def wrapper_foo(args):
    # print(*args)
    return foo(*args)


def foo(name, age, n):
    n = n*2
    greeting = f'hi {name}, you are {age}'
    # if name == 'fancy':
    #     time.sleep(1)
    print(f'{n}, {greeting}')
    return n, greeting


def wrapper_bar(args):
    print("run wrapper_bar")
    return bar(*args)


def bar(url, num):
    fake = Faker()
    profile1 = fake.simple_profile()
    p = Person()  # each thread holds an individual instance
    p.name = profile1.get('name')
    p.birthday = profile1.get('birthdate')
    with lock:
        persons.append(p)
    response = requests.get(url)
    return response.text, num


def all_urls():
    global url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('a')
    for i, link in enumerate(links):
        if 'cudnn' in link.get('href').lower():
            print(f"http://scdvstransfer.nvidia.com{link.get('href')}")


@timer_func
def multi_thread_pool():
    fake = Faker()
    names = []
    ages = []
    num = []
    for i in range(20):
        names.append(fake.name())
        ages.append(random.randint(0, 80))
        num.append(i)
    pool = ThreadPool(5)
    # launch thread
    # for i in range(4):
    #     pool.apply_async(foo, args=(name[i], age[i]))
    # another way to launch thread, passing more than 1 arg
    outputs = pool.map(bar, cudnn_urls)
    # outputs = pool.map_async(bar, cudnn_urls)
    # output = pool.map(wrapper_bar, zip(num, names))
    # for i in range(20):
    #     pool.apply_async(bar, args=([1]))
        # pool.apply(foo, args=(names[i], ages[i], num[i]))
        # pool.apply_async(wrapper_popen, args=(cmd[i], buff_log[i]))
    # pool.map(wrapper_popen, zip(cmd, buff_log))
    pool.close()
    pool.join()
    # for i in cudnn_urls:
    #     print(requests.get(i).text)


address_list = []
def multi_thread_with_lock_wrapper(args):
    return multi_thread_with_lock(*args)


def multi_thread_with_lock(n):
    fake = Faker()
    profile1 = fake.simple_profile()
    lock.acquire()
    address_list.append(profile1.address)
    lock.release()
    return


def demo_thread_poll_executor():
    # refer to https://superfastpython.com/threadpoolexecutor-map-vs-submit/
    x = len(cudnn_urls)
    thread_num = [i for i in range(x)]
    pool = ThreadPoolExecutor(max_workers=5)
    results = pool.map(wrapper_bar, zip(cudnn_urls, thread_num))

    # for res in results:
    #     print(res)
    pool.shutdown()


if __name__ == '__main__':
    # multi_thread_pool()
    demo_thread_poll_executor()
    print('done main')
