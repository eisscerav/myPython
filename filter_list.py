from faker import Faker


def demo():
    my_list = []
    for _ in range(100):
        fake = Faker()
        profile1 = fake.simple_profile()
        my_list.append(profile1.get('name'))
    er_filter = filter(lambda name: 'er' in name, my_list)
    er_list = list(er_filter)
    print('done demo filter list')


if __name__ == '__main__':
    demo()
