import base64
import slack
import os
import subprocess


def write_to_file(contents, file_name):
    with open(file_name, 'w') as fp:
        fp.writelines(contents)


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode()
    err = err.decode()
    if p.returncode:
        print(f'Error message: {err}')
        raise RuntimeError(f'Fail to run {cmd} with return code {p.returncode}')
    return out


def notify(channel, msg):
    # todo: may configure token as env variable and use os.environ['SLACK_TOKEN']
    encode_tok = b'your_token'
    token = base64.b64decode(encode_tok).decode()
    client = slack.WebClient(token)
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=msg
        )
        print(response)
    except slack.errors.SlackApiError as e:
        print(e)


if __name__ == '__main__':
    channel = '#my-bot'
    # os.system("sudo dhclient ens6")  # ens6 is network interface in test-thinkstation
    ip_ad = run_cmd('dhclient ens6')
    write_to_file(ip_ad, 'ip_ad.txt')
    print('done')
    # notify(channel, ip_ad)
