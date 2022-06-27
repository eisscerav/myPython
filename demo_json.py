import json


def read_json(file='data/coverage_history_results_A100.json'):
    with open(file, 'r') as fp:
        data = json.load(fp)
    print('done read_json')


if __name__ == '__main__':
    read_json()
