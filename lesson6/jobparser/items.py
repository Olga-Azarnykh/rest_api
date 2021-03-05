# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    link = scrapy.Field()
    link_hh = scrapy.Field()
    description = scrapy.Field()
    link_superjob = scrapy.Field()
    vacancies_links = scrapy.Field()
    _id = scrapy.Field()
