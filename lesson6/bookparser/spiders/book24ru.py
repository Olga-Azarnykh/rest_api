import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class  Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']

    #start_urls = ['https://book24.ru/search/?q=books#catalog-products']
    #start_urls = ['https://book24.ru/search/?q=books#book-list']
    start_urls = ['https://book24.ru/search/?q=books']

    def parse(self,response:HtmlResponse):

        #next_page = response.xpath('//a[@class="catalog-pagination__item _text js-pagination-catalog-item"]/@href').extract_first()
        #next_page = response.xpath('//button[@class="button _block _action js-load-more"]/@data-next-url').extract_first()

        next_page = response.xpath('//button[@class ="button js-pagination-catalog-item _load-more _block"]/@ data-href').extract_first()
        book_link = response.xpath('//a[@class="book-preview__image-link"]/@href').extract()
        for link in book_link:
            yield response.follow(link,callback=self.book_parse)

        if next_page:
            yield response.follow(next_page,callback=self.parse)
        else:
            return

    def book_parse(self,response:HtmlResponse):

        item_ref = response.url
        item_name = response.xpath('//span[@class="breadcrumbs__link"]/text()').extract_first()
        #item_autor = response.xpath('//div[@class="item-tab__chars-list"]/span/text()').extract_first()
        item_autor = response.xpath('//div[@class="item-tab__chars-list"]/div/span/a/text()').extract()[0]
        item_price = response.xpath('//div[@class="item-actions__price-old"]/text()').extract_first()
        item_price_disc = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
        item_rating = response.xpath('//div[@class="rating__rate-value _bold"]/text()').extract_first()

        yield BookparserItem(href=item_ref,name=item_name,autor = item_autor,price=item_price,
                             price_disc=item_price_disc,item_rating=item_rating)

        print('')
    print('')