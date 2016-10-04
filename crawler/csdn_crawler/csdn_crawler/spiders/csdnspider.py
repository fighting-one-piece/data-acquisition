# -*- coding:utf-8 -*-

import sys
import scrapy
from scrapy import Selector

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class CSDNSpider(scrapy.Spider):

    name = "csdn_spider"
    allowed_domains = ["csdn.net"]
    start_urls = ["http://geek.csdn.net/"]

    def parse(self, response):
        selector = Selector(response)
        print selector.xpath('//*[@id="geek_list"]/dl/dd/span[2]/a/text()').extract()

    def start_requests(self):
        login_url = 'http://passport.csdn.net/account/login'
        heads = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
        return [scrapy.Request(
            url=login_url,
            meta={'cookiejar': 1},
            callback=self.post_login
        )]

    def post_login(self, response):
        print 'preparing login'
        heads = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
        lt = Selector(response).xpath('//*[@id="fm1"]/input[3]/@value').extract()[0]
        print lt
        execution = Selector(response).xpath('//*[@id="fm1"]/input[4]/@value').extract()[0]
        print execution
        _eventId = Selector(response).xpath('//*[@id="fm1"]/input[5]/@value').extract()[0]
        print _eventId
        return [scrapy.FormRequest.from_response(response,
                         formdata={
                             'username': '125906088@qq.com',
                             'password': '@wulin5201314',
                             'rememberMe': True,
                             'lt': lt,
                             'execution': execution,
                             '_eventId': _eventId
                         },
                         # heads=heads,
                         # meta={'cookiejar': response.meta['cookiejar']},
                         callback=self.after_login
                         # dont_filter=True
                 )]

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)