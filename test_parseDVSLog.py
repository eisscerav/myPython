import os

from bs4 import BeautifulSoup
import requests
import re

user = 'ffan'
password = ''


class Config:
    def __init__(self, os, branch, cpu, gpu, test_suite, link):
        # self.config = config
        self.os = os
        self.branch = branch
        self.cpu = cpu
        self.gpu = gpu
        self.test_suite = test_suite
        self.existing_bug_id = -1
        self.link = link

    def set_bug_id(self, bug_id):
        self.existing_bug_id = bug_id


class TestResult:
    def __init__(self, cmd, fist_err, layer):
        self.cudnn_cmd = cmd
        self.fist_error = fist_err
        self.layer = layer

    def print_format(self):
        print(r'='*100)


def query_cudnn_bugs():
    pass


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
            current_case = text.replace(running_sym, '')
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
    test_results = r'test_results.log'
    global user
    global password
    url = r'http://scvrlweb.nvidia.com/list_result_files.php?job={}'.format(job_id)
    # test_results = r'test_results.log'  # todo: make reusable
    response = requests.get(url, auth=(user, password))
    soup = BeautifulSoup(response.text, 'lxml')
    all_links = soup.find_all('a')
    try:
        os.remove(test_results)
    except Exception as e:
        print(e)

    for link in all_links:
        if link.text == test_results:
            # todo: download test_results.log, eg, axel link
            download_link = link.get('href')
            cmd = r'axel -q {}'.format(download_link)
            print('Starting {}'.format(cmd))
            os.system(cmd)
            print('Download {} done'.format(download_link))
            return test_results
    print('done get_test_result')
    return 'no such file: {}'.format(test_results)


def parse_dvs_job(changelist='3116903139432407.0'):
    # todo: query nvbugs first and catch dup failing cases
    try:
        os.mkdir('tmp')
    except Exception as e:
        print(e)
    configs = []
    global user
    global password
    job_link = r'http://scdvs.nvidia.com/Regression_Results?which_changelist={}&which_category=Extended+Sanity'.format(changelist)
    response = requests.get(job_link, auth=(user, password))
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
                    # todo: may need a refactor by using config
                    config = Config(os_, branch, cpu, gpu, test_suite, job_link)
                    failing_cases = parse_cudnn_test_log(result_file)
                    # todo: save result into database
                    with open('tmp/{}.txt'.format(job_id), 'w') as f:
                        f.write('os,branch,cpu,gpu,test_suite,link,layer,err_msg\n')
                        for fail_case in failing_cases:
                            # print("os: {}, branch: {}, cpu: {}, gpu: {}, test_suite: {}, link: {}, cmd: {}, layer: {}, err: {}".format(
                            #     os_, branch, cpu, gpu, test_suite, job_link, fail_case.cudnn_cmd, fail_case.layer, fail_case.fist_error))
                            f.write(r'{},{},{},{},{},{},{},{},{}\n'.format(os_, branch, cpu, gpu, test_suite, job_link, fail_case.cudnn_cmd, fail_case.layer, fail_case.fist_error))
                            # f.write(f'{os_},{branch},{cpu},{gpu},{test_suite},{job_link},{fail_case.cudnn_cmd},{fail_case.layer},{fail_case.fist_error}')
                else:  # todo: to parse general error
                    pass
                print('Failing suite: {config},\t {test_suite},\t {job_link}'.format(config=gpu, test_suite=test_suite, job_link=job_link))
    print('done parse_job')


def main():
    # todo: parse existing bug
    # parse_cudnn_test_log()
    parse_dvs_job()


if __name__ == '__main__':
    main()
