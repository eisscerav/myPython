import subprocess
import os
from argparse_exer import save_env


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    if p.returncode:
        print(f'Error message: {err}')
        raise RuntimeError(f'Fail to run {cmd} with return code {p.returncode}')
    return out


# todo: add demo for subprocess.run()
def demo_sub_run():
    save_env('subprocess_env.txt')
    # p1 = subprocess.run(["python3", "argparse_exer.py", "--family", "nvidia"], check=True)
    p1 = subprocess.run('python3 argparse_exer.py --family ffan', check=True, shell=True)
    ret = p1.returncode
    output = p1.stdout
    args = p1.args
    print(p1)


def demo_sub_popen():
    os.environ['COMP'] = 'nvidia'
    env = os.environ
    save_env('subprocess_env.txt')
    cmd = 'python3 argparse_exer.py --family nvidia --name ampere --env_name sub_popen.txt'
    cmd = 'ls -l'
    cmd = 'p4 info'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # p = subprocess.Popen(cmd_list, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout = p.stdout.readlines()  # return a list(looks like separate by newline) and no output later in communicate
    # stderr = p.stderr.readlines()
    # Use communicate() rather than .stdin.write, .stdout.read or .stderr.read to avoid deadlock
    out, err = p.communicate()  # wait for child to finish and return string
    # output = out.decode()  # no need to decode with text=True
    if p.returncode:
        # stderr = err.decode() # no need to decode with text=True
        raise RuntimeError(f'Fail to run {p.args} with {err}')
    # p.kill()

    print(p)


if __name__ == '__main__':
    # demo_sub_run()
    demo_sub_popen()
