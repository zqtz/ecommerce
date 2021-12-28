import scrapy
from dangdang.items import DangdangItem


class DdSpider(scrapy.Spider):
    name = 'dd'
    # allowed_domains = ['www.dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=python%C5%C0%B3%E6&act=input&page_index=1']

    def parse(self, response):
        item = DangdangItem()
        li_lists = response.xpath('//*[@id="component_59"]/li')
        for li_list in li_lists:
            title = li_list.xpath('./p[1]/a/@title').extract()[0]
            link = 'http:'+li_list.xpath('./p[1]/a/@href').extract()[0]
            price = li_list.xpath('./p[3]/span/text()').extract()[0]
            shop = li_list.xpath('./p[4]/a/text()').extract()[0]
            item['title'] = title
            item['link'] = link
            item['price'] = price
            item['shop'] = shop
            # print(title)
            # print(link)
            # print(price)
            # print(shop)
            # print('*'*100)
            yield item

        for page in range(2,101):
            url = f'http://search.dangdang.com/?key=python%C5%C0%B3%E6&act=input&page_index={page}'
            result = scrapy.Request(url,callback=self.parse)
            yield result

