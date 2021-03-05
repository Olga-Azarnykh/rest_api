import scrapy

from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

tag_nextpages = "//a [@title='Следующая']/@href"

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    #start_urls = ['https://www.labirint.ru/books/']

    #start_urls = ['https://www.labirint.ru/search/%D0%BA%D0%BD%D0%B8%D0%B3%D0%B8/?stype = 0']
    start_urls = ['https://www.labirint.ru/search/books/?stype = 0']
    #start_urls = ['https://www.labirint.ru/search/?stype = 0']


    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        book_link = response.xpath("//div[@class='product-cover__cover-wrapper']/a/@href").extract()

        for link in book_link:
            yield response.follow(link,callback=self.book_parse)

        #print(next_page)
        #print(f'next-page {next_page}')

        if next_page:
            yield response.follow(next_page,callback=self.parse)
        else:
            return

        print('')

    def book_parse(self,response:HtmlResponse):
        #print()

        item_ref = response.url
        item_name = response.xpath('//h1//text()').extract_first()
        item_autor = response.xpath("//a[@data-event-label='author']/@data-event-content").extract_first()
        item_price = response.xpath('//div[@class="buying-priceold"]/div[@class="buying-priceold-val"]/span[@class="buying-priceold-val-number"]//text()').extract_first()
        item_price_disc = response.xpath('//div[@class="buying-pricenew-val"]/span[@class="buying-pricenew-val-number"]//text()').extract_first()
        item_rating = response.xpath('//div[@class="left"]/div[@id="rate"]//text()').extract_first()

        yield BookparserItem(href=item_ref,name=item_name,autor = item_autor,price=item_price,
                             price_disc=item_price_disc,item_rating=item_rating)
        print()
