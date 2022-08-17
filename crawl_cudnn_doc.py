from bs4 import BeautifulSoup
import requests

cudnn_doc_url = 'https://docs.nvidia.com/deeplearning/cudnn/api/index.html'


def parse_cudnn_api(section_number='3.2'):
    response = requests.get(cudnn_doc_url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_h3 = soup.find_all('h3', class_='title topictitle2')
    pub_api = []
    for h3 in all_h3:
        a = h3.a
        if h3.a.text.startswith(section_number):
            kbd = h3.find('kbd', class_='ph userinput')
            if kbd:
                # print(kbd.text)
                pub_api.append(kbd.text+'\n')
    with open('out.txt', 'w') as f:
        f.writelines(pub_api)
    print('done parse_cudnn_api')


def main():
    # section 4.1: ops_train, 5.2: cnn_infer, 6.2: cnn_train, 7.2: adv_infer, 8.2: adv_train
    section = {
        'ops_infer': '3.2',
        'ops_train': '4.1',
        'cnn_infer': '5.2',
        'cnn_train': '6.2',
        'adv_infer': '7.2',
        'adv_train': '8.2',
    }
    parse_cudnn_api(section.get('adv_train'))


if __name__ == '__main__':
    main()
