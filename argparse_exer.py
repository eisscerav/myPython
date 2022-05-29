import argparse
import os


def save_env(env_name):
    env = ''
    with open(env_name, 'w') as fp:
        for k in os.environ:
           str_ = f'{k}={os.environ[k]}\n'
           env += str_
           # print(str_)
        fp.writelines(env)


def demo_argparse():
    parser = argparse.ArgumentParser(description='name')
    parser.add_argument('--family', type=str, help='first name')
    parser.add_argument('--name', type=str, dest='ffan_name', metavar='meta', help='last name')
    parser.add_argument('--env_name', type=str, default='argparse_env.txt', help='save as env_name.txt')
    args = parser.parse_args()

    print(f"args.family={args.family}, args.ffan_name={args.ffan_name}")
    save_env(args.env_name)
    # parser.print_help()
    # parser.print_usage()


if __name__ == '__main__':
    demo_argparse()
