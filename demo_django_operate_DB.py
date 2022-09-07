import os
import sys
import subprocess
import random
import json
from faker import Faker
subprocess.run(f'{sys.executable} -m pip install django', shell=True)
subprocess.run(f'{sys.executable} -m pip install mysqlclient', shell=True)
import django
sys.path.append(r"/home/ffan/VC_on_cudnn_Win_remote/cudnn_site")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cudnn_site.settings')
django.setup()
from vectorcast.models import Person, ModuleCov, CovData, OverallCov  # set django env var and call setup first then import models


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


def convert_to_json():
    all_cov_data = CovData.objects.all()
    all_cov_data_list = []
    for cov_data in all_cov_data:
        module_cov = cov_data.modulecov_set.all()
        module_cov_data = {}
        module_cov_list = []
        for each in module_cov:
            print(each)
            module_cov_data['bcov_count'] = each.bcov_count
            module_cov_data['bcov_per'] = each.bcov_per
            module_cov_data['bcov_total'] = each.bcov_total
            module_cov_data['lcov_count'] = each.lcov_count
            module_cov_data['lcov_per'] = each.lcov_per
            module_cov_data['lcov_total'] = each.lcov_total
            module_cov_data['name'] = each.name
            module_cov_data['page'] = each.page
            module_cov_list.append(module_cov_data)
        overall_cov = cov_data.overallcov
        overall_cov_data = {'bcov_count': overall_cov.bcov_count, 'bcov_per': overall_cov.bcov_per,
                            'bcov_total': overall_cov.bcov_total, 'lcov_count': overall_cov.lcov_count,
                            'lcov_per': overall_cov.lcov_per, 'lcov_total': overall_cov.lcov_total,
                            'name': overall_cov.name, 'page': overall_cov.page}
        print(overall_cov)
        cov_data_d = {}
        cov_data_d['cudnn_version_cl'] = cov_data.cudnn_version_cl
        cov_data_d['cudnn_branch'] = cov_data.cudnn_branch
        cov_data_d['cudnn_cl'] = cov_data.cudnn_cl
        cov_data_d['cudnn_version'] = cov_data.cudnn_version
        cov_data_d['cuda_version'] = cov_data.cuda_version
        cov_data_d['report_date'] = cov_data.report_date.strftime("%Y-%m-%d")
        cov_data_d['report_link'] = cov_data.report_link
        cov_data_d['vectorcast_version'] = cov_data.vectorcast_version
        cov_data_d['file_num'] = cov_data.file_num
        cov_data_d['test_set'] = cov_data.test_set
        cov_data_d['test_num'] = cov_data.test_num
        cov_data_d['layer_file'] = cov_data.layer_file
        cov_data_d['label_file'] = cov_data.label_file
        # module_coverage, overall_coverage
        cov_data_d['module_coverage'] = module_cov_data
        cov_data_d['overall_coverage'] = overall_cov_data
        cov_data_d['total_tests_added'] = cov_data.total_tests_added
        cov_data_d['total_bugs_filed'] = cov_data.total_bugs_filed
        print(cov_data)
        all_cov_data_list.append(cov_data_d)
    with open('history.json', 'w') as f:
        json.dump(all_cov_data_list, f, indent=4, sort_keys=False)
    print('done convert_to_json')


if __name__ == '__main__':
    python = sys.executable
    print(python)
    convert_to_json()
    # get_report_data()
    # generate_persons()
