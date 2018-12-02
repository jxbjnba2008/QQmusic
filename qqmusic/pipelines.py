# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class QqmusicPipeline(object):
    def __init__(self):
        #连接mongodb
        self.connect = MongoClient(host='localhost',port=27017)
        #建立数据库qqmusic
        self.spider = self.connect.qqmusic
        #建立集合qqmusicdata
        self.col = self.spider.qqmusicdata
    def process_item(self, item, spider):
        self.col.insert({'singer':item['singer'],'song':item['song'],'albumname':item['albumname'],'time':item['time'],'download_url':item['download_url']})
        return item
