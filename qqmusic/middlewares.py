# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
import time
from scrapy.http import HtmlResponse

class QqmusicDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        '''无窗口化启动'''
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
    def process_request(self, request, spider):
        '''获取动态页面的源码''' 
        #对歌手列表页面使用selenium，每个歌手全部歌曲的页面不使用selenium，有助于获得结构化数据
        if 'singermid' not in request.url:     
            print('#'*30 + '中间件' + '*'*30)
            driver = webdriver.Chrome(options=self.options)
            # time.sleep(2)
            # driver.set_window_size(1280,720)
            time.sleep(2)
            # driver.maximize_window()
            driver.get(request.url)
            driver.execute_script('window.scrollBy(0,800)')
            time.sleep(2)
            body = driver.page_source   #取出源码
            return HtmlResponse(url=driver.current_url,body=body,encoding='utf-8',request=request)

