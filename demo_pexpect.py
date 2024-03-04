import pexpect
import os


def scp(files):
    if os.path.isdir(files):
        # send_files = "scp -r %s swqa@hostinfo.nvidia.com:/home/swqa/sw/cudnn_vectorcast_report/builds/" % files
        send_files = "scp -r %s cudnn@dlswqa-nas:/mnt/dlswqa_pool/cudnn/cudnn_vectorcast_report/builds/" % files
    else:
        # send_files = "scp -p %s swqa@hostinfo.nvidia.com:/home/swqa/sw/cudnn_vectorcast_report/builds/" % files
        send_files = "scp -p %s cudnn@dlswqa-nas:/mnt/dlswqa_pool/cudnn/cudnn_vectorcast_report/builds/" % files

    print(send_files)
    try:
        child = pexpect.spawn(send_files.format(files), timeout=3000)
    except AttributeError:
        child = pexpect.spawn(send_files.format(files), timeout=3000)
    index = child.expect(["Are you sure you want to", "password:", pexpect.EOF])
    if index == 0:
        child.sendline("yes")
        index = child.expect(["password:", pexpect.EOF], timeout=None)
        if index == 0:
            # child.sendline("labuser")
            child.sendline("cudnnuser")
    elif index == 1:
        # child.sendline("labuser")
        child.sendline("cudnnuser")
    else:
        child.sendline("exit")
    index = child.expect([pexpect.EOF], timeout=None)
    if index == 0:
        print("Successfully uploaded")
    else:
        raise RuntimeError("Scp failed")
    child.sendline("exit")


def demo():
    output = pexpect.run('df -h').decode('utf-8')
    child = pexpect.spawn('df -h')
    ret = child.expect(pexpect.EOF)
    out1 = child.before.decode('utf-8')

    print('done demo')


if __name__ == '__main__':
    scp('demo_pytorch')
    demo()