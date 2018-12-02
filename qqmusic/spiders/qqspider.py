# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from qqmusic.items import QqmusicItem
from scrapy.http import Request
import requests
import json,re,math

class QqspiderSpider(CrawlSpider):
    name = 'qqspider'
    allowed_domains = ['y.qq.com']
    page = 1
    url = 'https://y.qq.com/portal/singer_list.html#page='
    start_urls = [url + str(page)]

    def parse(self, response):
        '''通过selenium获取所有qq音乐歌手唯一标识singermid'''
        #首页的带图标的歌手
        singermid_list2 = response.xpath('//*[@id="mod-singerlist"]/div[1]/ul/li/div/a/@data-singermid').extract()
        #获取歌手列表
        singermid_list1 = response.xpath('//*[@id="mod-singerlist"]/ul/li/a/@data-singermid').extract()
        if singermid_list2:
            singermid_list1.extend(singermid_list2)
        #通过singermid获取歌手URL，进入歌手页面，这里只获取前两个歌手
        for singermid in singermid_list1:
            #歌手页面初始URL
            singer_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=981608482&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid={}&order=listen&begin=0&num=30&songstatus=1'.format(singermid)
            #Request的get请求歌曲页面
            yield Request(singer_url,callback=self.song_parse)
        #获取下一页的歌手列表
        if self.page<297:
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
            item['albumname'] = song['musicData']['albumname']
            item['time'] = song['musicData']['interval']
            #获取歌曲唯一标识songmid
            songmid = song['musicData']['songmid']
            #对歌曲播放链接进行请求获取下载的链接
            re = requests.get('https://u.y.qq.com/cgi-bin/musicu.fcg?g_tk=1086724312&loginUin=981608482&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%226992874192%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%226992874192%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%22981608482%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A981608482%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv%22%3A0%7D%7D'.format(songmid))
            js = json.loads(re.content)
            purl = js['req_0']['data']['midurlinfo'][0]['purl']
            download_url = 'http://dl.stream.qqmusic.qq.com/{}'.format(purl)
            item['download_url'] = download_url
            yield item
        #计算每个歌手的歌曲总页数
        pages = math.ceil(int(total)/30)
        for begin in range(pages):
            url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=981608482&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid={}&order=listen&begin={}&num=30&songstatus=1'.format(singermid,begin)
            yield Request(url,callback=self.song_parse)