from bs4 import BeautifulSoup
import requests
import base64
import shutil
import timeit
import time
import os
import threading


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


# todo: make get_cudnn_package reusable by adding parameters
def get_cudnn_package(pkg_url=r'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_dev_gpgpu_cuda_a_Release_Linux_Ubuntu20_04_AMD64_CUDNN_TESTS/'):
    homedir = os.path.expanduser(r'~')
    workdir = os.path.join(homedir, 'cudnn_pkg')
    try:
        os.mkdir(workdir)
    except Exception as e:
        print(e.strerror)
    os.chdir(workdir)
    base_url = r'http://scdvstransfer.nvidia.com'
    # cudnn_pkg_url = r'http://scdvstransfer.nvidia.com/dvsshare/vol2/cudnn_dev_gpgpu_cuda_a_Release_Linux_Ubuntu20_04_AMD64_CUDNN_TESTS/'
    response = requests.get(pkg_url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('a')
    pkgs = []
    for link in links:
        href = link.get('href')
        if href.endswith('TESTS.tgz') and 'fail' not in href.lower():  # ignore failing pkg
            pkgs.append(link.get('href'))
    latest_pkg = pkgs[-1]
    file_name = latest_pkg.split(r'/')[-1]
    local_files = os.listdir()
    local_pkgs = []
    need_to_download = True
    for local_file in local_files:
        # fixme: only remove cudnn_dev pkg here, make reusable
        if local_file.endswith('tgz') and 'cudnn_dev' in local_file and 'Ubuntu20_04' in local_file:
            local_pkgs.append(local_file)
        if local_file == file_name:
            need_to_download = False
    if need_to_download:
        down_link = '{}{}'.format(base_url, latest_pkg)
        print('Download pkg link : {}'.format(down_link))
        cmd = r'axel {} -o {}'.format(latest_pkg, file_name)  # accelerate download
        # print(cmd)
        with requests.get(down_link) as r:
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
        print('Done download')
        for pkg in local_pkgs:
            os.remove(pkg)
    else:
        print('No need to download cudnn packages from server\n')


def get_test_result(file_name=''):
    user = 'ffan'
    password = os.environ.get('NVPASSWORD')
    url = r'http://scvrlweb.nvidia.com/list_result_files.php?job=8688253'
    file_name = r'test_results.log'
    test_results = '{}/{}'.format(url, file_name)
    response = requests.get(url, auth=(user, password))
    soup = BeautifulSoup(response.text, 'lxml')
    all_links = soup.find_all('a')
    for link in all_links:
        if link.text == file_name:
            print(test_results)
    print('done req_non_exist')


def get_cask_bin(cuda='cuda11.7', arch='x86_64', OS='linux', size_type='minimal'):
    # fixme: move to a separate function
    homedir = os.path.expanduser(r'~')
    workdir = os.path.join(homedir, 'cudnn_pkg')
    try:
        os.mkdir(workdir)
    except Exception as e:
        print(e.strerror)
    os.chdir(workdir)
    # todo: make reusable by adding parameters
    user = 'ffan'
    password = base64.b64decode(os.environ.get('NVPASSWORD').encode())
    url = r'https://urm.nvidia.com/artifactory/sw-fastkernels-generic/cicd/cask_sdk/feature_5.0_cbi_cudnn/Nightly_for_CUDNN/'
    response = requests.get(url, auth=(user, password))
    if 200 <= response.status_code < 300:
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a')
        links.pop(0)  # remove href '../'
        new = 0  # todo: we only try to download the newest pkg, in case we need more cask pkgs
        for link in links:
            curr = int(link.get('href')[:-1])
            if curr > new:
                new = curr
            # print(link.get('href'))
        latest_cask_url = ''.join([url, str(new), r'/'])
        response_1 = requests.get(latest_cask_url, auth=(user, password))  # fixme: check response status_code
        soup_1 = BeautifulSoup(response_1.text, 'lxml')
        links_1 = soup_1.find_all('a')
        for link in links_1:
            if cuda in link.text and arch in link.text and size_type in link.text and OS in link.text:
                down_link = ''.join([latest_cask_url, link.text])
                filename = down_link.split('/')[-1]
                if filename not in os.listdir():
                    print(f'start to download {down_link}')
                    # with open(filename, 'w'):
                    #     pass
                    with open('down.txt', 'w') as f:  # todo: do we need more log info?
                        f.write(down_link)
                    with requests.get(down_link, auth=(user, password)) as r:  # fixme: check response status_code
                        with open(filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=4096):
                                f.write(chunk)
                    # remove old cask file
                    for f in os.listdir():
                        if f != filename and 'cask_sdk' in f:
                            os.remove(f)
    print('done get_cask_bin')


def main():
    # download_file(url=url)
    # timer(func=download_file, arg1=url)
    # demo()
    # get_test_result()
    get_cudnn_package()
    # get_cask_bin()


if __name__ == '__main__':
    main()

