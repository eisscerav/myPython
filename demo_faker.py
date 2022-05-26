from faker import Faker


# refer to more samples: https://zetcode.com/python/faker/
# official doc: https://pypi.org/project/Faker/
def demo_fake():
    fake = Faker()
    name = fake.name()
    addr = fake.address()
    text = fake.text()
    age = fake.age()
    print('demo fake done!!')


if __name__ == '__main__':
    demo_fake()
