import json


def read_json(file='data/coverage_history_results_A100.json'):
    with open(file, 'r') as fp:
        json_data = json.load(fp)
    my_data = {'Abs_abstract': 1, 'fancy': 'nvidia'}
    json_data.update(my_data)
    print('done read_json')
    return json_data


def write_json(dict_data):
    with open('new.json', 'w') as f:
        json.dump(dict_data, f, indent=4)
    print('done dump_to_file')


if __name__ == '__main__':
    json_file = 'data/fusionGraphTests.json'
    data = read_json(json_file)
    write_json(data)
