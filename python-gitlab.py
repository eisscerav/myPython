import os
import subprocess
from io import StringIO
import sys
import argparse
subprocess.run(f'{sys.executable} -m pip install requests', shell=True)
subprocess.run(f'{sys.executable} -m pip install python-gitlab', shell=True)
import gitlab

dlfw = {
    # project_name: project_id
    'mxnet': 9754,
    'pytorch': 9703,
    'tensorflow': 9743
}

class JobResult:
    def __init__(self, job):
        self.job = job
        self.job_results = []

    def set_ret(self, results):
        self.job_results = results

    def print_script_error(self):
        print(f'{self.job.name}: Please see {self.job.web_url}')
        print(f"brief summary:")
        for each in self.job_results:
            print(each)
        print("*"*100)

    def print_other_error(self):
        print(f"{self.job.name}: {self.job.failure_reason} {self.job.web_url}")


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    if p.returncode:
        print(f'Error message: {err}')
        raise RuntimeError(f'Fail to run {cmd} with return code {p.returncode}')
    return out


def parse_pytorch_log(log):
    ret = []
    log_list = log.split("\n")
    for log in log_list:
        if "test" in log.lower() and "failed" in log.lower() and "passed" not in log.lower():
            if "expected failure" not in log and "skip" not in log:
                ret.append(log)
        if "AssertionError".lower() in log.lower():
            ret.append(log)
        if "Error response from daemon".lower() in log.lower():
            ret.append(log)
    return list(dict.fromkeys(ret))


def parse_mxnet_log(log):
    # todo: may use another rule to parse mxnet log
    return parse_pytorch_log(log)


def parse_tensorflow_log(log):
    # todo: may use another rule to parse tensorflow log
    return parse_pytorch_log(log)


def parse_dlfw_log(project_name, log):
    if project_name == "pytorch":
        return parse_pytorch_log(log)
    if project_name == "mxnet":
        return parse_mxnet_log(log)
    if project_name == "tensorflow":
        return parse_tensorflow_log(log)


# make a DIY job
def parse_job(job):
    job_res = JobResult(job)
    job_res.job_id = job.id
    job_res.test_name = job.name
    job_res.failure_reason = job.failure_reason
    job_res.log_url = job.web_url
    return job_res


def print_separate_line(symbol='*', amount=100):
    print(symbol*amount)


def parse_pipeline(pipelines_id=8710058, project='mxnet'):
    project_id = dlfw.get(project)
    token = os.environ.get('GITLAB_TOKEN')
    gl = gitlab.Gitlab(url='https://gitlab-master.nvidia.com', private_token=token)
    gl.auth()
    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipelines_id)
    jobs = pipeline.jobs.list(iterator=True)
    script_fails = []
    other_fails = []
    print("Start parsing pipeline...")
    for job in jobs:
        if job.status == 'failed':
            if "L0" not in job.name:
                continue
            if job.failure_reason == "script_failure":
                # todo: parse failing logs
                out = run_cmd(f'curl --location --header "PRIVATE-TOKEN: {token}" "https://gitlab-master.nvidia.com/api/v4/projects/{project_id}/jobs/{job.id}/trace"')
                ret = parse_dlfw_log(project.name, out)
                job_res = JobResult(job)
                job_res.set_ret(ret)
                script_fails.append(job_res)
            else:  # todo: may add more conditions
                other_fails.append(JobResult(job))
                # print(f"{job.name}: {job.failure_reason} {job.web_url}")
    print("List script errors")
    print_separate_line()
    for fail in script_fails:
        fail.print_script_error()
    print_separate_line("#")
    print("List other errors")
    print_separate_line()
    for fail in other_fails:
        fail.print_other_error()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='using gitlab-python to parse gitlib CICD logs')
    parser.add_argument('--pipeline_id', type=int, help='Specify pipeline id')
    parser.add_argument('--project', type=str, help='Specify one of project name; [mxnet, pytorch, tensorflow]')
    args = parser.parse_args()
    parse_pipeline(args.pipeline_id, args.project)
