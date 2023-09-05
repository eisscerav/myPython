import os
import sys
import subprocess
import random
import json
from faker import Faker
try:
    import django
except ImportError:
    subprocess.run(f'{sys.executable} -m pip install django', shell=True)
    subprocess.run(f'{sys.executable} -m pip install mysqlclient', shell=True)
sys.path.append(r"/home/ffan/pycharm_remote/vectorcast_on_cudnn/cudnn_site")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cudnn_site.settings')
django.setup()
from vectorcast.models import Person, ModuleCov, CovData, OverallCov  # set django env var and call setup first then import models


def look_for_persons():
    persons = Person.objects.all()
    for p in persons:
        print(p.name)


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
        p = Person(username=username, name=name, sex=sex, address=address, mail=mail, birthdate=birthdate, job=job,
                   phone=phone)
        p.save()


def get_report_data():
    cov_data = CovData.objects.filter(cudnn_cl__exact='31670583')
    cov_data = CovData.objects.get(pk=90)
    module_cov = cov_data.modulecov_set.all()
    for each in  module_cov:
        print(each)
        each.delete()
    overall_cov = cov_data.overallcov
    overall_cov.delete()
    cov_data.delete()
    print('done')


def convert_data_to_json():
    all_cov_data = CovData.objects.all()
    all_cov_data_list = []
    for cov_data in all_cov_data:
        module_cov = cov_data.modulecov_set.all()
        module_cov_list = []
        for each in module_cov:
            print(each)
            module_cov_data = {'bcov_count': each.bcov_count, 'bcov_per': each.bcov_per, 'bcov_total': each.bcov_total,
                               'lcov_count': each.lcov_count, 'lcov_per': each.lcov_per, 'lcov_total': each.lcov_total,
                               'name': each.name, 'page': each.page}
            module_cov_list.append(module_cov_data)
        overall_cov = cov_data.overallcov
        overall_cov_data = {'bcov_count': overall_cov.bcov_count, 'bcov_per': overall_cov.bcov_per,
                            'bcov_total': overall_cov.bcov_total, 'lcov_count': overall_cov.lcov_count,
                            'lcov_per': overall_cov.lcov_per, 'lcov_total': overall_cov.lcov_total,
                            'name': overall_cov.name, 'page': overall_cov.page}
        print(overall_cov)
        cov_data_d = {'cudnn_version_cl': cov_data.cudnn_version_cl, 'cudnn_branch': cov_data.cudnn_branch,
                      'cudnn_cl': cov_data.cudnn_cl, 'cudnn_version': cov_data.cudnn_version,
                      'cuda_version': int(cov_data.cuda_version),
                      'report_date': cov_data.report_date.strftime("%Y-%m-%d"), 'report_link': cov_data.report_link,
                      'vectorcast_version': cov_data.vectorcast_version, 'file_num': cov_data.file_num,
                      'test_set': cov_data.test_set, 'test_num': cov_data.test_num, 'layer_file': cov_data.layer_file,
                      'label_file': cov_data.label_file, 'module_coverage': module_cov_list,
                      'overall_coverage': overall_cov_data, 'total_tests_added': cov_data.total_tests_added,
                      'total_bugs_filed': cov_data.total_bugs_filed}
        # module_coverage, overall_coverage
        print(cov_data)
        all_cov_data_list.append(cov_data_d)
    with open('history.json', 'w') as f:
        json.dump(all_cov_data_list, f, indent=4, sort_keys=False)
    print('done convert_to_json')


if __name__ == '__main__':
    python = sys.executable
    print(python)
    # convert_data_to_json()
    # get_report_data()
    # look_for_persons()
    generate_persons()
