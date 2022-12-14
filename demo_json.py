import json


def read_json(file='data/coverage_history_results_A100.json'):
    try:
        with open(file, 'r') as fp:
            json_data = json.load(fp)
        # my_data = {'Abs_abstract': 1, 'fancy': 'nvidia'}
        # json_data.update(my_data)
        # print('done read_json')
    except json.JSONDecodeError as e:
        json_data = {}
    except Exception:
        raise RuntimeError("Fail to decode json file")
    return json_data


def dump_json(dict_data):
    with open('new.json', 'w') as f:
        json.dump(dict_data, f, indent=4)
    print('done dump_to_file')


if __name__ == '__main__':
    json_file = 'data/fusionGraphTests.json'
    file2 = 'data/fusion.json'
    data = read_json(json_file)
    data2 = read_json(file2)
    data.update(data2)
    data = {}
    if data:
        dump_json(data)
