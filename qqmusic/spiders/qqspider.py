# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from qqmusic.items import QqmusicItem
from scrapy.http import Request
import json,re,math

class QqspiderSpider(CrawlSpider):
    name = 'qqspider'
    allowed_domains = ['y.qq.com']
    page = 1
    url = 'https://y.qq.com/portal/singer_list.html#page='
    start_urls = [url + str(page)]

    def parse(self, response):
        '''通过selenium获取所有qq音乐歌手唯一标识singermid'''
        
        #获取歌手列表
        singermid_list = response.xpath('//*[@id="mod-singerlist"]/ul/li/a/@data-singermid').extract()
        
        #通过singermid获取歌手URL，进入歌手页面
        for singermid in singermid_list[0:2]:
            #歌手页面初始URL
            singer_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=981608482&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid={}&order=listen&begin=0&num=30&songstatus=1'.format(singermid)
            #Request的get请求歌曲页面
            yield Request(singer_url,callback=self.song_parse)
        #获取下一页的歌手列表
        if self.page<3:
            self.page += 1
        yield Request(self.url+str(self.page),callback=self.parse)

    def song_parse(self,response):
        '''进入歌手页面获取歌手所有歌曲'''
        print('*'*30 + '获取歌曲' + '*'*30)
        #json格式数据转化
        data = json.loads(response.text)
        #获得歌曲信息以及歌手信息
        total = data['data']['total']
        song_list = data['data']['list'] 
        singermid = data['data']['singer_mid']
        for song in song_list:
            item = QqmusicItem()
            item['singer'] = data['data']['singer_name']
            item['song'] = song['musicData']['songname']
            yield item
        #计算每个歌手的歌曲总页数
        pages = math.ceil(int(total)/30)
        for begin in range(pages):
            url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=981608482&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid={}&order=listen&begin={}&num=30&songstatus=1'.format(singermid,begin)
            yield Request(url,callback=self.song_parse)