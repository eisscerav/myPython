import requests
from requests.auth import HTTPBasicAuth
import json
import os

# user = r'nvidia.com\ffan'  # Your Nvidia NTAccount
user = r'ffan'  # Your Nvidia NTAccount
password = os.environ.get('NVPASSWORD')  # Your Nvidia Password


class CudnnBug:
    def __init__(self, bug_id=-1):
        self.bug_id = bug_id
        self.failing_cmd = []

    def set_bug_id(self, bug_id):
        self.bug_id = bug_id

    def add_failing_cmd(self, cmd):
        self.failing_cmd.append(cmd)


def get_bug(bug_id=3470737):
    bug_id = 3542339
    url = "https://nvbugsapi.nvidia.com/nvbugswebserviceapi/api/bug/getbug/{}".format(bug_id)
    token = os.environ.get('NVBUGS_TOKEN_FFAN')
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    # response = requests.get(url, auth=HTTPBasicAuth(user, password))
    response = requests.get(url, headers=headers)
    content = response.content
    failing_case = []
    data = json.loads(response.text)
    bug_detail = data.get('ReturnValue')
    comments = bug_detail.get('Comments')
    desc = bug_detail.get('Description').split('\n')
    cudnn_bug = CudnnBug(bug_id)
    # for each in desc:
    #     if 'cudnnTest' in each:
    #         nvbug.add_failing_cmd(each.strip())
    reqDate = bug_detail.get('RequestDate')
    # description = data['ReturnValue']['DescriptionPlainTextReadOnly'] # todo use dict.get()
    # invalid_data = data.get('noneExist')
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
    print(response.status_code)
    return cudnn_bug


def get_nvbugs():
    # refer https://confluence.nvidia.com/display/NVBUG/GetBugs+API
    url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page=1&limit=100"
    # url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs"
    token = os.environ.get("NVBUGS_TOKEN")
    headers = {'Content-type': 'application/json',
               'Authorization': "Bearer " + token}

    # data = [
    #     {"FieldName": "BugRequesterFullName",   "FieldValue": "Fancy Fan"},
    #     {"FieldName": "ModuleName",             "FieldValue": "CUDA CUDNN"}
    # ]
    data = [
        {'FieldName': 'ModuleName', 'FieldValue': 'CUDA CUDNN'},
        {'FieldName': 'BugAction', 'FieldValue': 'Dev - Open - Blocked OR Dev - Open - To fix OR Dev - Open - To integrate OR Dev - Open - To Triage OR QA - Open - Provide more detail OR QA - Open - Request details from customer OR QA - Open - Verify new bug OR QA - Open - Verify to close'},
    ]

    payload = json.dumps(data)
    # response = requests.post(url, data=payload, auth=HTTPBasicAuth(user, password), headers=headers)
    response = requests.post(url, data=payload, headers=headers)
    toJson = response.json()
    # for key in toJson:
    #     print("key: {}, value:{}".format(key, toJson[key]))
    total = toJson.get('TotalCount')
    pages = -1
    bug_id = []
    if total/100:
        pages = int(total/100)+1
    else:
        pages = total/100
    for i in range(pages):
        url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page={}&limit=100".format(str(i+1))
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(user, password), headers=headers)
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


if __name__ == '__main__':
    # get_bug()
    get_nvbugs()
