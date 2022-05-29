import subprocess
import os
from argparse_exer import save_env


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
    # p = subprocess.Popen(['python3', 'argparse_exer.py', '--family', 'fan'], shell=True, env=env)
    cmd = 'python3 argparse_exer.py --family ffan --env_name sub_popen.txt'
    p = subprocess.Popen(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    poll = p.poll()
    out, err = p.communicate()
    if poll == 0:
        output = out.decode()
    else:
        raise RuntimeError(f'Fail to run {p.args}')
    # comm = p.communicate()
    print(p)


if __name__ == '__main__':
    # demo_sub_run()
    demo_sub_popen()
