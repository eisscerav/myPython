import requests
from requests.auth import HTTPBasicAuth
import json

user = r'nvidia.com\ffan'  # Your Nvidia NTAccount
password = "your_password"  # Your Nvidia Password


def getBug(bug_id=3470737):
    url = "https://nvbugsapi.nvidia.com/nvbugswebserviceapi/api/bug/getbug/{}".format(bug_id)
    response = requests.get(url, auth=HTTPBasicAuth(user, password))
    content = response.content
    failing_case = []
    data = json.loads(response.text)
    bug_detail = data.get('ReturnValue')
    comments = bug_detail.get('Comments')
    desc = bug_detail.get('Description')
    reqDate = bug_detail.get('RequestDate')
    # description = data['ReturnValue']['DescriptionPlainTextReadOnly'] # todo use dict.get()
    invalid_data = data.get('noneExist')
    bug_description = data.get('ReturnValue').get('DescriptionPlainTextReadOnly')
    # read string one by one line
    for each in bug_description.splitlines():
        print(each)
        if "cudnnTest" in each:
            failing_case.append(each)
    print(response.content)


def getBugs():
    url = r"https://nvbugsapi.nvidia.com/NVBugsWebServiceApi/api/Search/GetBugs?page=1&limit=10"
    headers = {'Content-type': 'application/json'}

    data = [
        {"FieldName": "BugRequesterFullName",   "FieldValue": "Fancy Fan"},
        {"FieldName": "ModuleName",             "FieldValue": "CUDA CUDNN"}
    ]

    payload = json.dumps(data)
    response = requests.post(url, data=payload, auth=HTTPBasicAuth(user, password), headers=headers)
    toJson = response.json()
    for key in toJson:
        print("key: {}, value:{}".format(key, toJson[key]))

    bugs = toJson.get("ReturnValue")
    bug_ids = []
    for idx, bug in enumerate(bugs):
        bug_ids.append(bug.get("BugId"))
    # todo: We have bug ids and then can handle bug by getBug web api one by one to get more details
    #  (eg,. bug description and comments)
    totalCount = toJson.get("TotalCount")

    print("TotalCount = ", totalCount)
    print(bugs)


if __name__ == '__main__':
    getBug()
    getBugs()
