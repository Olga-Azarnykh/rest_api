from pprint import pprint
import requests
from lxml import html
import sys
sys.stdout.encoding
import json

def out_news(curr_Cro):
    result = []
    items = dom.xpath(curr_Cro)

    for item in items:
        curr_res={}
        #забираем новость, заголовок и дату
        if link == "https://lenta.ru":
            linknews = link
            href = item.xpath(".//a/@href")
            #обход блогов
            if href[0][0:5] == 'https':
                continue
            if (href[0][0:10] == '/ themes /') or (href[0][0:8] == '/themes/'):
                continue

            href=link+href[0]
            response_href = requests.get(href,headers=header)
            dom_href = html.fromstring(response_href.text)

            #извлекаем заголовок
            topik = dom_href.xpath("//h1/text()")
            topik = topik[0].replace('\xa0', ' ')

            #извлекаем дату
            b_topiks = dom_href.xpath("//div[@class='b-topic__info']")
            for b_topik in b_topiks:
                data_news = b_topik.xpath("//time[@class ='g-date']/@datetime")
            data_news = data_news[0]
            #извлекаем тело новости
            body = dom_href.xpath("//div[contains( @class ,'b-text')]/p//text()")
            bodynews=""
            for curr_str in body:
                bodynews = bodynews+curr_str
        elif link=='https://yandex.ru/news':
            if curr_Cro == "//article[contains(@class,'mg-card mg-card_flexible')]":
                curr_parenth = item.xpath("..")
                #href= curr_parenth.xpath(".//a//@href")
                #linknews = curr_parenth.xpath(".//a//@aria-label")
                #linknews = linknews[0]
                #data_news = curr_parenth.xpath(".//a//@data -log -id")[0]
                href=item.xpath("..//a//@href")[0]
                linknews = item.xpath("..//a//@aria-label")[0]
                data_news = item.xpath("..//a//@data-log-id")[0]
            else:
                href = item.xpath(".//a//@href")[0]
                #href = href[0]
                #href = item.xpath(".//a/@href")
                linknews = item.xpath(".//a//@aria-label")[0]
                #linknews = linknews[0]
                data_news = item.xpath(".//a//@data-log-id")[0]

            topik = item.xpath(".//h2/text()")
            topik = topik[0]
            bodynews = item.xpath(".//div[@class='mg-card__annotation']/text()")
            bodynews = bodynews[0]

        curr_res['href'] = href
        curr_res['topik'] = topik
        curr_res['body'] = bodynews
        curr_res['data_news'] = data_news
        curr_res['source'] = linknews

        result.append(curr_res)
    return result


header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

#lenta.ru
link = "https://lenta.ru"
response = requests.get(link,headers=header)

dom = html.fromstring(response.text)

news = out_news("//div[@class='b-feature__header']|//div[@class='titles']|//div[@class='item']|//div[contains(@class,'b-tabloid__topic')]")

lenta_news = json.dumps(news, indent=1, ensure_ascii=False)
pprint(lenta_news)

#item
#titles
#b-feature__header
#item news b-tabloid__topic_news
#b-tabloid__topic article !!!
#b-tabloid__topic news b-tabloid__topic_news

#yandex.ru
news = ''
link = ''
response = ''

link = "https://yandex.ru/news"
response = requests.get(link,headers=header)
dom = html.fromstring(response.text)



#news = out_news("//div[@class='mg-card__inner']|//article[contains(@class,'mg-card mg-card_flexible')]")
news1 = out_news("//div[@class='mg-card__inner']")  #первая новость
news2 = out_news("//article[contains(@class,'mg-card mg-card_flexible')]") #остальные новости

#pprint(news1)
#pprint(news2)
ya_news1 = json.dumps(news1, indent=1, ensure_ascii=False)
pprint(ya_news1)
ya_news2 = json.dumps(news2, indent=1, ensure_ascii=False)
pprint(ya_news2)


