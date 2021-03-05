from typing import List
import scrapy
import self as self
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://voronezh.superjob.ru/vakansii/sistemnyj-administrator.html']
    urls = ['https://voronezh.superjob.ru']

    def parse(self, response: HtmlResponse):
        #  pass
        next_page = response.xpath("//a[@class='icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        vacancies_links = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacansy_parse(self, response: HtmlResponse):
        item_block = response.xpath("//h1/text()").extract()
        if len(item_block) == 1:
            item_name = ''
            i = 0
            while i < len(item_block):
                item_name = item_name + item_block[i]
                i = i + 1
            else:
                item_name = item_block[0]

        item_salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        item_salary_min = 0
        item_salary_max = 0
        if item_salary[0].strip() == 'По договорённости':
            pass
        else:
            if item_salary[0].strip() == 'от':
                item_salary_min = int(item_salary[2].replace('\xa0', '').replace('руб.', ''))
            if item_salary[2].strip() == 'до':
                item_salary_max = int(item_salary[5].replace('\xa0', '').replace('руб.', ''))
            else:
                if item_salary[0].strip() == 'до':
                    item_salary_max = int(item_salary[2].replace('\xa0', '').replace('руб.', ''))
                else:
                    if item_salary[0].strip() != 'от':
                        item_salary_min = int(item_salary[0].replace('\xa0', ''))
                        item_salary_max = int(item_salary[1].replace('\xa0', ''))

    #    item_link = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']//a//@href").extract_first()
        item_link = response.url
        item_link_superjob = self.allowed_domains[0]
        yield JobparserItem(name=item_name,  salary_min=item_salary_min, salary_max=item_salary_max, link=item_link, link_superjob=item_link_superjob)

        print()

