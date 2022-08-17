from bs4 import BeautifulSoup
import requests

cudnn_doc_url = 'https://docs.nvidia.com/deeplearning/cudnn/api/index.html'


def parse_cudnn_api(section_number='3.2'):
    response = requests.get(cudnn_doc_url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_h3 = soup.find_all('h3', class_='title topictitle2')
    for h3 in all_h3:
        a = h3.a
        if h3.a.text.startswith(section_number):
            kbd = h3.find('kbd', class_='ph userinput')
            if kbd:
                print(kbd.text)

    print('done parse_op_infer_api')


def main():
    # section 4.2: ops_train, 5.2: cnn_infer, 6.2: cnn_train, 7.2: adv_infer, 8.2: adv_train
    parse_cudnn_api('4.2')


if __name__ == '__main__':
    main()
