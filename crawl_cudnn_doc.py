from bs4 import BeautifulSoup
import requests

cudnn_doc_url = 'https://docs.nvidia.com/deeplearning/cudnn/api/index.html'
section = {
    'ops_infer': '3.2',
    'ops_train': '4.1',
    'cnn_infer': '5.2',
    'cnn_train': '6.2',
    'adv_infer': '7.2',
    'adv_train': '8.2',
}
deprecated = 'This function has been deprecated in cuDNN'
class CUDNN_API:
    api_name = ''
    is_deprecated = False


def parse_cudnn_api(soup, section_number='3.2'):
    # response = requests.get(cudnn_doc_url)
    # soup = BeautifulSoup(response.text, 'lxml')
    all_h3 = soup.find_all('h3', class_='title topictitle2')
    pub_api = []
    for h3 in all_h3:
        a = h3.a
        if h3.a.text.startswith(section_number):
            kbd = h3.find('kbd', class_='ph userinput')
            if kbd: # should be API name
                cudnn_api = CUDNN_API()
                cudnn_api.api_name = kbd.text.replace('()', '')
                # pub_api.append(api_name)
                all_p = h3.parent.find_all('p')
                for p in all_p:
                    if deprecated in p.text:
                        cudnn_api.is_deprecated = True
                        break
                pub_api.append(cudnn_api)
                # pub_api.append(api_name+'\n')
            # else:  # should be title
            #     name = h3.a.get('name')
            #     pub_api.append(name+'\n')
    # with open(section_number+'_out.txt', 'w') as f:
    #     f.writelines(pub_api)
    # print(f'done parse_cudnn_api for {section_number}')
    return pub_api


def get_soup():
    response = requests.get(cudnn_doc_url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_cudnn_api():
    soup = get_soup()
    # parse_cudnn_api_v2(soup)
    pub_api = []
    # section 4.1: ops_train, 5.2: cnn_infer, 6.2: cnn_train, 7.2: adv_infer, 8.2: adv_train
    for k, v in section.items():
        pub_api += parse_cudnn_api(soup, v)
    return pub_api


def main():
    get_cudnn_api()


if __name__ == '__main__':
    main()
