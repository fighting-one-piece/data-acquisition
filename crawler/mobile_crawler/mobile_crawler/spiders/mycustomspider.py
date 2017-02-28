# -*- coding: utf-8 -*-

import sys
import scrapy
import traceback
import threading
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.queue import SpiderPriorityQueue

mutex = threading.Lock()

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class MobileSingleSpider(RedisCrawlSpider):

    name = "custom_spider"
    allowed_domains = ["iteye.com"]
    redis_key = 'custom_spider:imcaller'

    # start_urls = ('http://www.iteye.com/news/32170','http://www.iteye.com/news/32169')

    def __init__(self):
        print 'scrapy init'

    def start_requests(self):
        print 'scrapy start requests'
        request = scrapy.Request(
            url='http://www.iteye.com/news/32140',
            headers={
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                'Set-Cookie': '_javaeye3_session_=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNoSGFzaHsABjoKQHVzZWR7ADoMdXNlcl9pZGkDK28TOg9zZXNzaW9uX2lkIiU2ZWI4NGUxMWEwNWZjY2M0ZDNmMzRlOWY4YzgyYTUwNzoLYXV0aGVkewc6DXByb3ZpZGVyIgljc2RuOgh1aWQiEXd1bGluc2hpc2hlbjoQX2NzcmZfdG9rZW4iMWN0dnVzclEwSkg3VzljNE1BNzQxMHlXYnJ4NDFXR0tWdmFaRkc2eEhzY2s9--d913b35b93cbc173670bc3abc0f951ef6070d5f4; domain=.iteye.com; path=/; HttpOnly',
            }
        )
        yield request


    def parse(self, response):
        print 'scrapy parse response'
        try:
            print response.body
        except Exception, e:
            print e.message
            print traceback.format_exc()