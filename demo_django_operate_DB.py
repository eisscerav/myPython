import os
import sys
import subprocess
import random
from faker import Faker
subprocess.run(f'{sys.executable} -m pip install django', shell=True)
subprocess.run(f'{sys.executable} -m pip install mysqlclient', shell=True)
import django
sys.path.append(r"/home/test/pycharm_remote/cudnn_site")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cudnn_site.settings')
django.setup()
from vectorcast.models import Person  # set django env var and call setup first then import models


def generate_persons():
    fake = Faker()
    print("Generate fake data for table Person...")
    num_of_person = random.randint(1, 5)
    for _ in range(num_of_person):
        profile = fake.profile()
        username = profile.get('username')
        name = profile.get('name')
        sex = profile.get('sex')
        address = profile.get('address')
        mail = profile.get('mail')
        birthdate = profile.get('birthdate')
        job = profile.get('job')
        phone = fake.phone_number()
        p = Person(username=username, name=name, sex=sex, address=address, mail=mail, birthdate=birthdate, job=job, phone=phone)
        p.save()


if __name__ == '__main__':
    python = sys.executable
    print(python)
    generate_persons()
