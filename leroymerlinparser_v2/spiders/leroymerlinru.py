import scrapy

from leroymerlinparser.items import LeroymerlinparserItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%BB%D0%B0%D0%BC%D0%BF%D0%B0']
    urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@class="paginator-button next-paginator-button"]/@href').extract_first()
        # ads_links = response.xpath("//source[@media='(min-width: 1200px)']/@srcset")

        ads_links = response.xpath("//product-card/@data-product-url").extract()

        # ads_links=response.xpath('//a[@class="plp-item__info__title"]/href')

        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def parse_ads(self, response: HtmlResponse):
        # url = response.url
        self.driver.get(response.url)
        # name = response.xpath('//h1[@class="header-2"]/text()').extract()[0]

        name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        product_description = response.xpath('//dt[@class="def-list__term"]//text()').extract()

        product_detail = response.xpath('//dd[@class="def-list__definition"]//text()').extract()

        # product_n = []
        # for n in product_detail:
        #    product_n.append(n.replace('\n', '').replace(' ', ''))
        #    print(n)
        # product_detail = product_n

        price = response.xpath('//span[@slot="price"]//text()').extract()[0]

        thumbs = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="product-content"]'))
        )

        photos = [i.find_element_by_xpath("//img[@slot='thumbs']").get_attribute('src') for i in
                  thumbs]  # Извлекаем из каждого объекта ссылку на фотку

        yield (LeroymerlinparserItem(name=name, photos=photos, product_description=product_description,
                                     product_detail=product_detail, price=price))
