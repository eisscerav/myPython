import requests
import shutil
import timeit
import time


def timer():
    start = timeit.default_timer()
    time.sleep(5)
    stop = timeit.default_timer()
    print('Time: ', stop - start)


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


if __name__ == '__main__':
    print('Start download_file')
    url = r'http://scdvstransfer.nvidia.com/dvsshare/vol2/cuda_dev_Release_Linux_AMD64_GPGPU_CUDA_CUFFT/SW_31014917.0_cuda_dev_Release_Linux_AMD64_GPGPU_CUDA_CUFFT.tgz'
    # download_file(url=url)
    timer()
    print('Done download_file')

