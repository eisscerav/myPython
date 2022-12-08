import pandas


def name_list():
    df = pandas.read_csv(r'd:\github\name_list.csv', encoding='GBK')
    ori_name = pandas.read_csv(r'd:\github\ori_name.csv', encoding='GBK')
    print('done name_list')


if __name__ == '__main__':
    name_list()
