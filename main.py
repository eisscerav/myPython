# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os, json, re


def print_hi(name):
    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    num  = (1,2,3,4,5,6,7,8,9,0)
    correct_pred = {classname: 0 for classname in classes}
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+Shift+B to toggle the breakpoint.

def get_total_bugs_filed(keywords):  # keywords is a list
    if keywords is None:
        return 0
    import requests
    # from requests.auth import HTTPBasicAuth
    # user = r'svc_dlswqa'
    # encode_pwd = b'WXY4S0t4SkckSkR5'
    # password = base64.b64decode(encode_pwd).decode()
    token = os.environ.get('NVBUGS_TOKEN_FFAN')
    url = "https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page=1&limit=2000"
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer '+token
               }
    bug_filter = [
        {"FieldName": "ModuleName", "FieldValue": "CUDA CUDNN"},
        {"FieldName": "CustomKeyword", "FieldValue": " AND ".join(keywords)},
        {"FieldName": "BusinessUnit", "FieldValue": "Tesla"},
        {"FieldName": "Disposition", "FieldValue": "*Open* OR *Fixed* OR *Will not fix* OR *Fix unknown*"}
    ]
    response = requests.post(url, data=json.dumps(bug_filter),
                             headers=headers).json()
                             # auth=HTTPBasicAuth(user, password), headers=headers).json()
    if "IsSuccess" in response and response["IsSuccess"]:
        count = int(response["TotalCount"])
        # bugs = []
        # for bug in response["ReturnValue"]:
        #     bugs.append([str(bug["BugId"]), bug["Synopsis"]])
        return count
    else:
        print(response)
        print("nvbugs query failed!")
        return 0

def parse_pytorch_log(log):
    ret = []
    p1 = re.compile("(Running \d+ items in this shard)")
    p2 = re.compile(".*\bfail\b.*test.*", re.I)
    p3 = re.compile(".*test.*\bfail\b.*", re.I)
    p4 = re.compile(".*test.*\bfailed\b.*", re.I)
    p5 = re.compile(".*\bfailed\b.*test.*", re.I)
    log_list = log.split("\n")
    for log in log_list:
        log = re.sub("\[\s*\w+.\w+\]", "", log)
        log = re.sub("\[\s*\w+%\]", "", log)
        log_raw = log.strip()
        log = log.lower()
        m1 = re.search(p1, log)
        if m1:
            continue
        # m2 = re.search(p2, log)
        # m3 = re.search(p3, log)
        # m4 = re.search(p4, log)
        # m5 = re.search(p5, log)
        if "test" in log and ("failed" in log or "fail" in log):
            if "expected failure" not in log and "skip" not in log and "xfail" not in log and "passed" not in log and "warning" not in log:
        # if (m2 or m3 or m4 or m5) and "passed" not in log.lower():
        #     if "expected failure" and "skip" not in log.lower():
                ret.append(log_raw)
        if "AssertionError".lower() in log:
            ret.append(log_raw)
        if "Error response from daemon".lower() in log:
            ret.append(log_raw)
        if "TIMEOUT EXPIRED".lower() in log and "echo" not in log:
            ret.append(log_raw)
        if "[ERROR]" in log:
            ret.append(log_raw)
    return list(dict.fromkeys(ret))


def replace_str_in_src(src_file, _old, _new):
    new_content = []
    with open(src_file, 'r') as f:
        content = f.readlines()
        for line in content:
            m1 = re.search(_old, line)
            if m1:
                line = _new
            new_content.append(line)
    with open(src_file, 'w') as f:
        f.writelines(new_content)


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    s = "(Invalid argument to    call [NV_ERR_INVALID_ARGUMENT])"
    s1 = re.sub("\s+", " ", s)
    s1 = re.sub("[^a-zA-Z\d\s_:]", " AND ", s1).strip()
    s1 = re.sub("\s+", " AND ", s1)
    valueof_list = s.split("__##")
    # get_total_bugs_filed(["dlqa_testdev_codecoverage_newbug"])
    s = ["10.0.10", "9.0.2", "8.10.9", "9.0.1"]
    # cudnn_vers.sort(key=lambda s: list(map(int, s.split('.'))))
    s.sort(key=lambda e: list(map(int, e.split('.'))))
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
