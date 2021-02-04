from bs4 import BeautifulSoup as bs
import requests

import json
import sys

sys.stdout.encoding

from pprint import pprint

# https://www.superjob.ru/vakansii/povar-universal.html?geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=42
# https://www.superjob.ru/vakansii/povar-universal.html?geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=42&page=1
# https://www.superjob.ru/vakansii/povar-universal.html?geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=42&page=1
# https://www.superjob.ru/vacancy/search/?keywords= Повар&profession_only=1&geo[c][0]=15&geo[c][1]=1&geo[c][2]=9

url = 'https://www.superjob.ru'
ps_url = '/vacancy/search/'

my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Accept': '*/*'}
currpage = 1

vacancy = 'Программист'

my_params = {
    'keywords': vacancy,
    'profession_only': '1',
    'geo[c][0]': '15',
    'geo[c][1]': '1',
    'geo[c][2]': '9',
    'page': ''
}

response = requests.get(url + ps_url, params=my_params, headers=my_headers)

soup = bs(response.text, 'html.parser')

tag_page = soup.find('a', {'class': 'f-test-button-1'})
link_page = tag_page.contents[0].getText()

if not link_page:
    last_page = 1
else:
    tag_page = tag_page.findParent()
    last_page = int(tag_page.find_all('a')[-2].getText())

curr_dict = {}
out_dict = {}
out_lict = []

for page in range(0, last_page + 1):
    pprint(f'тек страница {page}')
    my_params['page'] = page

    response = requests.get(url + ps_url, params=my_params, headers=my_headers)
    soup = bs(response.text, 'html.parser')

    block_vacancy = soup.find_all('div', {'class': 'f-test-vacancy-item'})

    for vacancy in block_vacancy:
        # имя вакансии
        tag_name = vacancy.find_all('a')
        vacancy_name = tag_name[0].getText()
        # линк вакансии
        link_name = tag_name[0]['href']
        link_name = url + link_name

        # оплата
        block_span = vacancy.find('span', {'class': 'f-test-text-company-item-salary'})
        block_payment = block_span.getText()

        pre_pay = block_span.getText().replace('\xa0', ' ').split(' ', 1)[0]

        pay_str = block_span.contents[0].getText().replace('\xa0', ' ')
        pozition = pay_str.find('—', 0)

        carrency_list = pay_str.split(' ')
        carrency = carrency_list[len(carrency_list) - 1]

        if pre_pay == 'от':
            pay_minimum = pay_str[2:pozition - 1:][0:len(pay_str[2:pozition - 1:]) - 3]
            pay_minimum = pay_minimum.replace(' ', '')
            pay_maximum = '-'
        elif pre_pay == 'до':
            pay_minimum = '-'
            pay_maximum = pay_str[pozition + 1::]
            pay_maximum = pay_maximum[2::][0:len(pay_maximum[2::]) - 4]
            pay_maximum = pay_maximum.replace(' ', '')
        else:
            pay_minimum = pay_str[0:pozition - 1:].replace(' ', '')
            pay_maximum = pay_str[pozition + 1::]
            pay_maximum = pay_maximum[0:len(pay_maximum) - 4]
            pay_maximum = pay_maximum.replace(' ', '')

        curr_dict['name'] = vacancy_name
        curr_dict['href'] = link_name
        curr_dict['pay_minimum'] = pay_minimum
        curr_dict['pay_maximum'] = pay_maximum
        curr_dict['carrency'] = carrency

    out_lict.append(curr_dict)

    # pprint(f'{tag_name[0].getText()} {tag_name[1].getText()} {pay_minimum} {pay_maximum} {link_name}')

out_dict['response'] = out_lict
out_json1 = json.dumps(out_dict, indent=1, ensure_ascii=False)

pprint(out_json1)
