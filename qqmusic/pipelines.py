# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class QqmusicPipeline(object):
    def __init__(self):
        self.connect = MongoClient(host='localhost',port=27017)
        self.spider = self.connect.qqmusic
        self.col = self.spider.musicdata
    def process_item(self, item, spider):
        self.col.insert({'singer':item['singer'],'song':item['song']})
        return item
