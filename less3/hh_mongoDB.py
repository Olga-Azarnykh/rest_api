from bs4 import BeautifulSoup as bs
import requests
import json
import sys
sys.stdout.encoding

from pymongo import MongoClient
from pprint import pprint

def print_vacancy(mypay):
    #вывод вакансий подходящих под заданное условие
    result = None
    '''
    for m in vac_hh.find({'$or':[{'pay_minimum':{'$gte':mypay}},{'pay_maximum':{'$gte':mypay}}]},
                         {'name':True,'pay_maximum':True,'pay_minimum':True}):
        pprint(m)
        step = 1
    '''
    for m in vac_hh.find({'$or':
                              [{'pay_minimum':{'$gte':mypay}},
                               {'$and':[{'pay_maximum':{'$gte':mypay}},
                                         {'pay_minimum':{'$gte':mypay}}
                                        ]
                                 }
                               ]},
                         {'name':True,'href':True, 'pay_maximum':True,'pay_minimum':True}):
        pprint(m)
        step = 1



client = MongoClient('127.0.0.1',27017)

db = client['vacancy']
vac_hh = db.base_vac

#vac_hh.delete_many({})
#for m in vac_hh.find({}):
#    pprint(m)
#    step=1



url = 'https://hh.ru'

#https://hh.ru/search/vacancy?ares=26&fromSearchLine=True&st=searchVacancy&text=Python&from=suggest_post&page=0
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

#response = requests.get(url + '/search/vacancy/', params=my_params, headers=my_headers)
#response = requests.get(url + '/vacancies/prodavets-konsultant/', headers=my_headers)
# https://voronezh.hh.ru/search/vacancy?L_is_autosearch=false&area=26&clusters=true&enable_snippets=true&text=Python&page=2
response = requests.get(url + '/search/vacancy', params=my_params, headers=my_headers)
soup = bs(response.text, "html.parser")

curr_dict={}
out_dict={}
out_lict=[]

block_button = soup.find('span',{'class':'bloko-button-group'})
last_page = len(block_button.contents)

my_test=0
for page in range(0,last_page):
#    pprint(page)
    my_params['page'] = str(page)

    response = requests.get(url + '/search/vacancy', params=my_params, headers=my_headers)
    soup = bs(response.text, "html.parser")

    vacancy_list = soup.find_all('a', {'class': 'bloko-link HH-LinkModifier'})
#    pprint(vacancy_list)

    #+++тестовый ограничитель
    my_test=my_test+1
    if my_test==3:
        break
    #---

    for vacancy in vacancy_list:
        name_vacancy = vacancy.getText()
        href_vacancy = vacancy['href']
        block_pay = vacancy.parent.parent.parent.parent.parent

        #переходим на страницу с вакансией и забираем зарплату
        salary_resp = requests.get(href_vacancy,headers=my_headers)
        salary_soup = bs(salary_resp.text,"html.parser")
        block_pay = salary_soup.find('span',{'class':'bloko-header-2_lite'})
        #pprint(f'{name_vacancy}+{href_vacancy}+{block_pay.getText()}')
        block_pay = block_pay.getText()
        if block_pay == 'з/п не указана':
            paymin = 0
            paymax = 0
            currency = " - "
        else:
            pre_pay = block_pay.replace('\xa0', ' ').split(' ', 1)[0]
            #pozition = block_pay.find(' ', 0)
            if pre_pay == 'от':
                #'от 60 000 до 100 000 руб. на руки'
                pay = block_pay[2::].lstrip()

                paymin = pay[0:pay.find(" ",0)]

                tayl = pay[len(paymin):]
                paymin = float(paymin.replace('\xa0', ' ').replace(' ', ''))


                postpay = tayl.lstrip()
                postpay = postpay[0:postpay.find(" ",0)]
                if postpay=="до":
                    tayl = tayl.lstrip()[2::].lstrip()

                    paymax = tayl[0:tayl.find(" ",0)]
                    paymax = float(paymax.replace('\xa0', ' ').replace(' ', ''))

                    currency = tayl[tayl.find(" ",0):tayl.find(".",tayl.find(" ",0))]
                else:
                    paymax=0
                    currency = pay[pay.find(" ",0):pay.find(".",pay.find(" ",0))]
                #block_pay[2::].lstrip() block_pay[2::].lstrip().find(" ",0)
            elif pre_pay=='до':
                paymin = 0
                tayl = block_pay[2::].lstrip()
                paymax = tayl[:tayl.find(" ",0)]
                paymax = float(paymax.replace('\xa0', ' ').replace(' ', ''))
                currency = tayl[tayl.find(" ",0):tayl.find(".",tayl.find(" ",0))]
                #m = block_pay

            #else:
            #    m = block_pay

        if paymin ==0:
            #paymin = float(paymin)
            paymin = None
        if paymax ==0:
            #paymax = float(paymax)
            paymax = None
        if currency == " - ":
            currency = None

        #Формируем id вакансии
        _idvac = int(hash(href_vacancy))

        curr_dict={'_id':_idvac,'name':name_vacancy,'href':href_vacancy,
                   'pay_minimum':paymin,'pay_maximum':paymax,'currency':currency}

        out_lict.append(curr_dict)

        #result_find = add_rec(_idvac,curr_dict)
        #add_rec(_idvac, curr_dict)
        #vac_hh.insertOne()

        #Добавляем вакансию в базу
        vac_hh.replace_one({'_id':_idvac},curr_dict,upsert=True)
        step = 1
        '''
        result = False
        for vacant in vac_hh.find({'_idvac': {'$eq': _idvac}}, {'_id': True}):
            
            if vacant['_id'] == _idvac:
                reuslt = True
            ctep = 1

            pprint(vacant)

        if result == False:
            vac_hh.insert_one(curr_dict)
     
        for vacant in vac_hh.find():
            pprint(vacant)
        step=1
        '''
        #pprint(f'{name_vacancy} {href_vacancy} {paymin} {paymax} {currency}')

#for m in vac_hh.find({}):
#    pprint(m)
#    step=1


#print(out_lict)

#out_dict['response'] = out_lict

#out_json = json.dumps(curr_dict, indent=1, ensure_ascii=False)
#pprint(out_json)
#Сериализация json файл
#with open('hh_json.json', 'r') as f:
#    json.dump(out_json, f)


#vacant = db.vacancy.find({})
#pprint(vacant)
#step=1

inp_pay = input("Введите желаемую сумму зарплаты \n>>>")
inp_pay = float(inp_pay)
if inp_pay == 0:
    print('Введите сумму отличную от нуля')
else:
    print_vacancy(inp_pay )
