import pexpect
import os
import base64


def login_colossus(cmd, env_pwd):
    # child = pexpect.spawn(cmd, timeout=float(3000))
    child = pexpect.spawn(cmd, timeout=3000)
    index = child.expect(["User Name", pexpect.EOF])
    if index == 0:
        child.sendline("ffan")
        index = child.expect(["Password", pexpect.EOF])
        if index == 0:
            encode_pwd = os.environ.get(env_pwd)
            if encode_pwd:
                password = base64.b64decode(encode_pwd).decode()
                child.sendline(password)
                index = child.expect(["User Name", pexpect.EOF])
                if index == 0:
                    raise RuntimeError("Password is not correct!!!")
            else:
                raise RuntimeError("Fail to get password!!!")
    else:
        raise RuntimeError("Fail to login colossus!!!")
    index = child.expect([pexpect.EOF], timeout=None)
    if index == 0:
        print("Successfully login colossus")
    else:
        raise RuntimeError("login colossus failed")


def extend_lease():
    pass


if __name__ == "__main__":
    cmd = "/home/test/vpython-3.11/bin/python /home/test/vpython-3.11/bin/colossus login"
    login_colossus(cmd, "NVPASSWORD")
