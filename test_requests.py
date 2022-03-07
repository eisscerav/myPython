import requests
import shutil
import timeit
import time
import os


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


@timer_func
def download_file(url):
    local_filename = url.split('/')[-1]
    print(local_filename)
    # with requests.get(url, stream=True) as r:
    #     with open(local_filename, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    r = requests.get(url)

    return local_filename


if __name__ == '__main__':
    print('Start download_file')
    url = r'http://scdvstransfer.nvidia.com/dvsshare/vol2/cuda_dev_Release_Linux_AMD64_GPGPU_CUDA_CUFFT/SW_31031480.0_cuda_dev_Release_Linux_AMD64_GPGPU_CUDA_CUFFT.tgz'
    download_file(url=url)
    # timer(func=download_file, arg1=url)
    print('Done download_file')

