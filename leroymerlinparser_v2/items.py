# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    product_description = scrapy.Field()
    product_detail = scrapy.Field()

    product_n = []
    for n in product_detail:
        product_n.append(n.replace('\n', '').replace(' ', ''))
        print(n)
    product_detail = product_n

    _id = scrapy.Field()