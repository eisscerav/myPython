import re


def parse_log():
    layer_pattern = re.compile(r'Running test L.*:')
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
            failing_cases[current_case] = (error_msg, layer)

    for k, v in failing_cases.items():
        print('key: {k} value: {v}'.format(k=k, v=v))
    # with open('tmp.txt', 'w+') as f:
    #     for each in simple_contents:
    #         f.write(each)

    fp.close()


if __name__ == '__main__':
    parse_log()
