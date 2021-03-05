import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://voronezh.hh.ru/search/vacancy?area=26&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        #  pass
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        vacancies_links = response.css("a.bloko-link.HH-LinkModifier::attr(href)").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacansy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()

        item_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        item_salary_min = 0
        item_salary_max = 0
        if item_salary[0].strip() == 'з/п не указана':
            pass
        else:
            if item_salary[0].strip() == 'от':
                item_salary_min = int(item_salary[1].replace('\xa0', ''))
            if item_salary[2].strip() == 'до':
                item_salary_max = int(item_salary[3].replace('\xa0', ''))
            else:
                if item_salary[0].strip() == 'до':
                    item_salary_max = int(item_salary[1].replace('\xa0', ''))

        item_link = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract_first()
        item_link_hh = self.allowed_domains[0]
        yield JobparserItem(name=item_name, salary_min=item_salary_min, salary_max=item_salary_max, link=item_link, link_hh=item_link_hh)
        print()

