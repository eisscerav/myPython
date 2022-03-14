from ftplib import FTP


def demo():
    ftp = FTP('23.22.74.198')
    status = ftp.login()
    pwd = ftp.pwd()
    ftp.cwd('cmake-cookbook')
    file_list = ftp.retrlines('LIST')
    print(status)
    ftp.close()


if __name__ == '__main__':
    demo()
