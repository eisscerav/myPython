import os
from bs4 import BeautifulSoup
import requests
import re
import glob
import argparse
import shutil
import pandas as pd
import json

user = 'ffan'
password = os.environ.get('NVPASSWORD')


class CudnnBug:
    def __init__(self, bug_id=-1):
        self.bug_id = bug_id
        self.failing_cmd = []

    def set_bug_id(self, bug_id):
        self.bug_id = bug_id

    def add_failing_cmd(self, cmd):
        self.failing_cmd.append(cmd)


class Config:
    def __init__(self, os, branch, cpu, gpu, test_suite, link):
        # self.config = config
        self.os = os
        self.branch = branch
        self.cpu = cpu
        self.gpu = gpu
        self.test_suite = test_suite
        self.link = link


class TestResult:
    def __init__(self, cmd, fist_err, layer):
        self.cudnn_cmd = cmd
        self.fist_error = fist_err
        self.layer = layer
        self.existing_bug_id = -1

    def set_bug_id(self, bug_id):
        self.existing_bug_id = bug_id

    def print_format(self):
        print(r'='*100)


def get_bug(bug_id=3470737):
    url = r"https://nvbugsapi.nvidia.com/nvbugswebserviceapi/api/bug/getbug/{}".format(bug_id)
    response = requests.get(url, auth=(user, password))
    if response.status_code >=200 and response.status_code < 300:
        data = json.loads(response.text)
        bug_detail = data.get('ReturnValue')
        comments = bug_detail.get('Comments')
        cudnn_bug = CudnnBug(bug_id)
        bug_description = data.get('ReturnValue').get('Description')

        # read string one by one line
        for each in bug_description.splitlines():
            if "cudnnTest" in each:
                cudnn_bug.add_failing_cmd(each.strip())
        for comment in comments:
            texts = comment.get('CommentText').splitlines()
            for text in texts:
                if 'cudnnTest' in text:
                    cudnn_bug.add_failing_cmd(text.strip())
        return cudnn_bug
    else:
        print(f'Fail to visit bug {bug_id}, status_code={response.status_code}')


def query_cudnn_bugs():
    # todo: make more reusable
    # refer https://confluence.nvidia.com/display/NVBUG/GetBugs+API
    url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page=1&limit=100"
    headers = {'Content-type': 'application/json'}

    data = [
        {'FieldName': 'ModuleName', 'FieldValue': 'CUDA CUDNN'},
        # {'FieldName': 'BugAction',  'FieldValue': 'QA - Open - Verify new bug OR QA - Open - Verify to close'},
        {'FieldName': 'BugAction',  'FieldValue': 'Dev - Open - Blocked OR Dev - Open - To fix OR Dev - Open - To integrate OR Dev - Open - To Triage OR QA - Open - Provide more detail OR QA - Open - Request details from customer OR QA - Open - Verify new bug OR QA - Open - Verify to close'},
    ]

    payload = json.dumps(data)
    response = requests.post(url, data=payload, auth=(user, password), headers=headers)
    total = response.json().get('TotalCount')
    pages = -1
    bug_id = []
    if total / 100:
        pages = int(total / 100) + 1
    else:
        pages = total / 100
    for i in range(pages):
        url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page={}&limit=100".format(
            str(i + 1))
        response = requests.post(url, data=payload, auth=(user, password), headers=headers)
        bugs = response.json().get('ReturnValue')
        for bug in bugs:
            bug_id.append(bug.get('BugId'))
    bug_id = list(set(bug_id))
    # bugs = toJson.get("ReturnValue")
    # bug_ids = []
    # for idx, bug in enumerate(bugs):
    #     bug_ids.append(bug.get("BugId"))
    # todo: We have bug ids and then can handle bug by getBug web api one by one to get more details
    #  (eg,. bug description and comments)
    return bug_id


def parse_general_log(file_name=''):
    # todo: to implement
    pass


def parse_cudnn_test_log(file_name=r'/home/fanxin/Downloads/cudnn_triage/test_results.log'):
    layer_pattern = re.compile(r'Running test L.*:')
    pass_sym = r'&&&& PASSED '
    failed_sym = r'&&&& FAILED '
    running_sym = r'&&&& RUNNING '
    error_sym = r'@@@@ First error msg'
    debug_sym = r'[DEBUG]'
    fp = open(file_name, 'r')  # todo: make more reusable
    failing_cases = []  # {}
    contents = fp.readlines()
    current_case = ''
    error_msg = ''  # []
    layer = ''
    # case = ['test_name', 'error_msg', 'passed/failed']
    for idx,  text in enumerate(contents):
        if running_sym in text and 'cudnnTest' in text and r'-R' in text and debug_sym not in text:
            current_case = text.replace(running_sym, '').strip()
        m = layer_pattern.match(text.strip())
        if m:
            g = m.group(0)
            layer = g.replace('Running test ', '').replace(':', '').strip()
        if error_sym in text and debug_sym not in text:
            error_msg = text
        if failed_sym in text and debug_sym not in text and current_case in text:
            # failing_cases[current_case] = (error_msg, layer)
            failing_cases.append(TestResult(current_case, error_msg, layer))
    # for failing_case in failing_cases:
    #     print('cudnnTest: {}error message: {}layer: {}'.format
    #           (failing_case.cudnn_cmd, failing_case.fist_error, failing_case.layer))
    #     failing_case.print_format()
    fp.close()
    return failing_cases


def get_test_result(job_id='8688253'):
    test_result = r'test_results.log' # todo: make reusable
    global user
    global password
    url = r'http://scvrlweb.nvidia.com/list_result_files.php?job={}'.format(job_id)
    response = requests.get(url, auth=(user, password))
    soup = BeautifulSoup(response.text, 'lxml')
    all_links = soup.find_all('a')
    try:
        for result in glob.glob(r'test_results.log*'):
            os.remove(result)
    except Exception as e:
        print(e)

    for link in all_links:
        if link.text == test_result:
            # todo: download test_results.log, eg, axel link
            download_link = link.get('href')
            cmd = r'axel -q {}'.format(download_link)
            print('Starting {}'.format(cmd))
            os.system(cmd)
            print('Download {} done'.format(download_link))
            return test_result
    print('done get_test_result')
    return 'no such file: {}'.format(test_result)


def parse_dvs_changelist(argparser, changelist='3116903139432407.0'):
    # todo: query nvbugs first and catch dup failing cases
    cudnn_bugs = []
    bug_ids = query_cudnn_bugs()
    for bug_id in bug_ids:
        print(bug_id)
        cudnn_bug = get_bug(bug_id)
        if cudnn_bug.failing_cmd:
            cudnn_bugs.append(cudnn_bug)
    try:
        shutil.rmtree('tmp')
        os.mkdir('tmp')
    except Exception as e:
        print('create folder tmp')
        os.mkdir('tmp')
    configs = []
    global user
    global password
    job_link = r'http://scdvs.nvidia.com/Regression_Results?which_changelist={}&which_category=Extended+Sanity'.format(changelist)
    response = requests.get(job_link, auth=(user, password))
    if response.status_code >= 200 and response.status_code < 300:
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table', width="1080", border="0", cellspacing="0", cellpadding="0")
        for table in tables:
            test_suite = table.text.strip().split()[0]
            tables_cell_outline_1 = table.find_all('table', border="0", cellspacing="1", cellpadding="0", width="1080", class_="cell_outline_1")
            trs = tables_cell_outline_1[1].find_all('tr')
            for tr in trs:
                tr_tds = tr.find_all('td')
                test_result = tr_tds[9]
                contents = test_result.contents
                branch = tr_tds[0].text
                os_ = tr_tds[2].text
                cpu = tr_tds[3].text
                gpu = tr_tds[4].text
                if contents[0] == 'Build Failure':
                    print('Build Failure: {test_suite}, {branch}, {OS}, {cpu}, {gpu}'.format(test_suite=test_suite, branch=tr_tds[0].text, OS=tr_tds[2].text, cpu=tr_tds[3].text, gpu=tr_tds[4].text))
                    continue
                is_pass = test_result.a.text
                if 'Failure' in is_pass:  # no need to triage passing result
                    job_id = test_result.a.get('href')[-7:]
                    job_link = r'http://scvrlweb.nvidia.com/list_result_files.php?job={}'.format(job_id)
                    # todo: get_test_result() then parse log
                    result_file = get_test_result(job_id)
                    if 'no' not in result_file and 'CUDNN.LEVEL' in test_suite:  # to parse log in cudnnTest fashion
                    # if 1:
                        # todo: may need a refactor by using config
                        # config = Config(os_, branch, cpu, gpu, test_suite, job_link)
                        failing_cases = parse_cudnn_test_log(result_file)
                        # failing_cases = parse_cudnn_test_log()  # for debug
                        # todo: save result into database
                        # columns = ['os', 'branch', 'cpu', 'gpu', 'test_suite', 'link', 'cmd', 'layer', 'err_msg']
                        series_os = []
                        series_branch = []
                        series_cpu = []
                        series_gpu = []
                        series_test_suite = []
                        series_link = []
                        series_cmd = []
                        series_layer = []
                        series_errmsg = []
                        series_bug_id = []
                        for fail_case in failing_cases:
                            series_os.append(os_)
                            series_branch.append(branch)
                            series_cpu.append(cpu)
                            series_gpu.append(gpu)
                            series_test_suite.append(test_suite)
                            series_link.append(job_link)
                            series_cmd.append(fail_case.cudnn_cmd)
                            series_layer.append(fail_case.layer)
                            series_errmsg.append(fail_case.fist_error)
                            for bug in cudnn_bugs:
                                if fail_case.existing_bug_id != -1:
                                    break
                                for failing in bug.failing_cmd:
                                    if fail_case.cudnn_cmd in failing:
                                        fail_case.set_bug_id(bug.bug_id)
                                        break
                            series_bug_id.append(fail_case.existing_bug_id)
                            # todo: save bug_id into dataframe
                        data = {
                            'os': series_os,
                            'branch': series_branch,
                            'cpu': series_cpu,
                            'gpu': series_gpu,
                            'test_suite': series_test_suite,
                            'link': series_link,
                            'cmd': series_cmd,
                            'layer': series_layer,
                            'error_message': series_errmsg,
                            'bug_id': series_bug_id
                        }
                        df = pd.DataFrame(data)
                        df.to_csv('tmp/{}.csv'.format(job_id), index=False)
                        # with open('tmp/{}.csv'.format(job_id), 'w') as f:  # todo: use pandas
                        #     f.write('os,branch,cpu,gpu,test_suite,link,cmd,layer,err_msg\n')
                        #     for fail_case in failing_cases:
                                # f.write(f'{os_},{branch},{cpu},{gpu},{test_suite},{job_link},{fail_case.cudnn_cmd},{fail_case.layer},{fail_case.fist_error}')
                    else:  # todo: to parse general error
                        pass
                    print('Failing suite: {config},\t {test_suite},\t {job_link}'.format(config=gpu, test_suite=test_suite, job_link=job_link))
        print(f'Done: query changelist {changelist}')
    else:
        print(f'Fail to visit changelist {changelist}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str, default='ffan', help='nv account')
    parser.add_argument('--password', type=str, help='nv credential')
    # todo: parse existing bug
    # parse_cudnn_test_log()
    parse_dvs_changelist(argparser=parser)


if __name__ == '__main__':
    main()
