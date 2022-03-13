import requests
import shutil
import timeit
import time
import os
import threading
from bs4 import BeautifulSoup


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        stop = timeit.default_timer()
        print(f'Function {func.__name__!r} executed in {(stop-start):.4f}s')
        return result
    return wrap_func


def timer(func, arg1):
    start = timeit.default_timer()
    func(arg1)
    stop = timeit.default_timer()
    print('Time: ', stop - start)


def write_to_file(filename, chunksize):
    filename.write(chunksize)

@timer_func
def download_file(url=r'http://dvstransfer.nvidia.com/dvsshare/dvs-binaries/gpu_drv_cuda_a_Release_Linux_AMD64_GPGPU_COMPILER/SW_31051952.0_gpu_drv_cuda_a_Release_Linux_AMD64_GPGPU_COMPILER.tgz'):
    print('Start download_file')

    local_filename = url.split('/')[-1]
    print(local_filename)
    thread_lst = []
    response = requests.get(url, stream=True)
    # fp = open(local_filename, 'wb')
    # for chunk in response.iter_content(chunk_size=1024):
    #     t = threading.Thread(target=write_to_file, args=(fp, chunk))
    #     thread_lst.append(t)
    # for th in thread_lst:
    #     th.start()
    # for th in thread_lst:
    #     th.join()
    # fp.close()
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=4096):
            f.write(chunk)
    # with requests.get(url, stream=True) as r:
    #     with open(local_filename, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    # r = requests.get(url)

    print('Done download_file')
    return local_filename


def demo():
    response = requests.get(r'http://192.168.1.5:8088/', auth=('ffan', '1'))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
    print(response)


if __name__ == '__main__':
    url = r'http://dvstransfer.nvidia.com/dvsshare/dvs-binaries/gpu_drv_cuda_a_Release_Linux_AMD64_GPGPU_COMPILER/SW_31051952.0_gpu_drv_cuda_a_Release_Linux_AMD64_GPGPU_COMPILER.tgz'
    # download_file(url=url)
    # timer(func=download_file, arg1=url)
    demo()

