from bs4 import BeautifulSoup as bs
import requests
import json
import sys

sys.stdout.encoding

from pprint import pprint

# https://voronezh.hh.ru/vacancies/povar
# https://voronezh.hh.ru/search/vacancy?area=26&fromSearchLine=true&st=searchVacancy&text=Big+data&from=suggest_post
# https://voronezh.hh.ru/search/vacancy?area=26&fromSearchLine=true&st=searchVacancy&text=%D0%9F%D0%BE%D0%B2%D0%B0%D1%80&from=suggest_post&page=1
url = 'https://hh.ru'

# https://hh.ru/search/vacancy?ares=26&fromSearchLine=True&st=searchVacancy&text=Python&from=suggest_post&page=0
vacancy = 'Python'
pages = ''
my_params = {'area': '26',
             'fromSearchLine': 'true',
             'st': 'searchVacancy',
             'text': vacancy,
             'from': 'suggest_post',
             'page': pages}

my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Accept': '*/*'}

# response = requests.get(url + '/search/vacancy/', params=my_params, headers=my_headers)
# response = requests.get(url + '/vacancies/prodavets-konsultant/', headers=my_headers)
# https://voronezh.hh.ru/search/vacancy?L_is_autosearch=false&area=26&clusters=true&enable_snippets=true&text=Python&page=2
response = requests.get(url + '/search/vacancy', params=my_params, headers=my_headers)
soup = bs(response.text, "html.parser")

curr_dict = {}
out_dict = {}
out_lict = []

block_button = soup.find('span', {'class': 'bloko-button-group'})
last_page = len(block_button.contents)

for page in range(0, last_page):

    my_params['page'] = str(page)

    response = requests.get(url + '/search/vacancy', params=my_params, headers=my_headers)
    soup = bs(response.text, "html.parser")

    vacancy_list = soup.find_all('a', {'class': 'bloko-link HH-LinkModifier'})
    # pprint(vacancy_list)
    for vacancy in vacancy_list:
        name_vacancy = vacancy.getText()
        href_vacancy = vacancy['href']
        block_pay = vacancy.parent.parent.parent.parent.parent

        salary_resp = requests.get(href_vacancy, headers=my_headers)
        salary_soup = bs(salary_resp.text, "html.parser")
        block_pay = salary_soup.find('span', {'class': 'bloko-header-2_lite'})

        block_pay = block_pay.getText()
        if block_pay == 'з/п не указана':
            paymin = 0
            paymax = 0
            currency = " - "
        else:
            pre_pay = block_pay.replace('\xa0', ' ').split(' ', 1)[0]

            if pre_pay == 'от':

                pay = block_pay[2::].lstrip()
                paymin = pay[0:pay.find(" ", 0)]
                tayl = pay[len(paymin):]
                postpay = tayl.lstrip()
                postpay = postpay[0:postpay.find(" ", 0)]
                if postpay == "до":
                    tayl = tayl.lstrip()[2::].lstrip()
                    paymax = tayl[0:tayl.find(" ", 0)]
                    currency = tayl[tayl.find(" ", 0):tayl.find(".", tayl.find(" ", 0))]
                else:
                    paymax = 0
                    currency = pay[pay.find(" ", 0):pay.find(".", pay.find(" ", 0))]

            elif pre_pay == "до":
                paymin = 0
                tayl = block_pay[2::].lstrip()
                paymax = tayl[:tayl.find(" ", 0)]
                currency = tayl[tayl.find(" ", 0):tayl.find(".", tayl.find(" ", 0))]

        curr_dict['name'] = name_vacancy
        curr_dict['href'] = href_vacancy
        curr_dict['pay_minimum'] = paymin
        curr_dict['pay_maximum'] = paymax
        curr_dict['carrency'] = currency

        out_lict.append(curr_dict)

out_dict['response'] = out_lict
out_json1 = json.dumps(out_dict, indent=1, ensure_ascii=False)

pprint(out_json1)
