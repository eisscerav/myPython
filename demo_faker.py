from faker import Faker
import logging

# refer to more samples: https://zetcode.com/python/faker/
# official doc: https://pypi.org/project/Faker/
def demo_fake():
    fake = Faker()
    name = fake.name()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("Harmless debug Message")
    logging.info("Just an information")
    logging.warning("Its a Warning")
    logging.error("Did you try to divide by zero")
    logging.critical("Internet is down")
    addr = fake.address()
    text = fake.text()
    print('demo fake done!!')



if __name__ == '__main__':
    demo_fake()
