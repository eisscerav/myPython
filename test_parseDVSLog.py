import re


def parse_log():
    pass_sym = r'&&&& PASSED '
    failed_sym = r'&&&& FAILED '
    running_sym = r'&&&& RUNNING '
    error_sym = r'@@@@ First error msg'
    debug_sym = r'[DEBUG]'
    fp = open(r'/home/fanxin/Downloads/cudnn_triage/test_results.log', 'r')
    failing_cases = {}
    contents = fp.readlines()
    current_case = ''
    error_msg = '' #[]
    # case = ['test_name', 'error_msg', 'passed/failed']
    for idx,  text in enumerate(contents):
        if running_sym in text and 'cudnnTest -R' in text and debug_sym not in text:
            current_case = text.replace(running_sym, '')
        if error_sym in text and debug_sym not in text:
            error_msg = text
        if failed_sym in text and debug_sym not in text and current_case in text:
            failing_cases[current_case] = error_msg

    for k, v in failing_cases.items():
        print(k, v)
    # with open('tmp.txt', 'w+') as f:
    #     for each in simple_contents:
    #         f.write(each)

    fp.close()


if __name__ == '__main__':
    parse_log()
