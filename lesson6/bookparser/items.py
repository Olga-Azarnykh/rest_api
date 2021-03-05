# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    href = scrapy.Field()
    name = scrapy.Field()
    autor = scrapy.Field()
    price = scrapy.Field()
    price_disc = scrapy.Field()
    item_rating = scrapy.Field()
    _id = scrapy.Field()

    #print()


