import glob
import subprocess
import re
import os, sys
subprocess.run(f'{sys.executable} -m pip install p4python==2020.1.1983437', shell=True)
from P4 import P4
from crawl_cudnn_doc import get_cudnn_api

cudnn_dir = r'//sw/gpgpu/MachineLearning/cudnn'


class CheckAPIResult:
    api_name = ''
    result = ''


def get_p4_info():
    p4 = P4()
    p4.port = 'p4proxy-zj:2006'
    p4.user = 'ffan'
    p4.client = 'ffan_cudnn_client_1'
    info = ''
    try:
        p4.connect()
        info = p4.run('info')
    except Exception:
        print('Fail to connect to p4 server')
        exit(-1)
    return info


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    if not out and p.returncode == 1:
        return 'not found'
    if p.returncode:
        # stderr = err.decode() # no need to decode with text=True
        raise RuntimeError(f'Fail to run {p.args} with {err}')
    return out


def check_api_name(srcs, apis):
    for src in srcs:
        pass


def demo_glob():
    # pub_api = get_cudnn_api()
    info = get_p4_info()
    p4root = info[0].get('clientRoot')
    cudnn_localdir = p4root+cudnn_dir.replace('//', '/')
    # cu_files = glob.glob(cudnn_localdir+"/test/**/*.cu", recursive=True)
    cu_files = glob.glob(os.path.join(cudnn_localdir, 'test', '**', '*.cu'), recursive=True)
    cpp_files = glob.glob(cudnn_localdir+"/test/**/*.cpp", recursive=True)
    test_srcs = cu_files + cpp_files
    # check_api_name(test_srcs, pub_api)
    # for test_src in test_srcs:
    #     with open(test_src, 'r') as fp:
    #         content = fp.readlines()
    #         for line in content:
    #             # todo: check if api be present here
    #             pass
    print('done demo glob')


def get_grep_cmd(api_name):
    grep_str = r'ag "\b{}\b" -n'.format(api_name)
    # grep_str += r'.{h,cpp,cu}'
    return grep_str


if __name__ == '__main__':
    demo_glob()
    info = get_p4_info()
    p4root = info[0].get('clientRoot')
    cudnn_local_dir = p4root+cudnn_dir.replace('//', '/')
    cudnn_local_test_dir = os.path.join(cudnn_local_dir, 'test')
    os.chdir(cudnn_local_test_dir)
    cudnn_api = get_cudnn_api()
    result_list = []
    for api in cudnn_api:
        cmd = get_grep_cmd(api)
        output = run_cmd(cmd)
        res = CheckAPIResult()
        if output == 'not found':
            res.api_name = api
            res.result = 'not found'
            result_list.append(res)
        else:
            res.api_name = api
            res.result = 'found'
            result_list.append(res)
    for res in result_list:
        if res.result == 'not found':
            print(res.api_name)
