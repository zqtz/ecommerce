# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class DangdangPipeline:
    def __init__(self):
        self.client = MongoClient(host='localhost',port=27017)
        self.db = self.client['当当']
        self.collections = self.db['python爬虫']

    def process_item(self, item, spider):
        data = {
            'title': item['title'],
            'link': item['link'],
            'price': item['price'],
            'shop': item['shop'],
        }
        print(data)
        self.collections.insert(data)
        return item



    # def close_spider(self):
    #     self.collections.close()
