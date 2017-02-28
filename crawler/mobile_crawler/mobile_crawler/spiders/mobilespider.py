# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import random
import scrapy
import traceback
import threading
from mobilecrypt import crypt
from mobile_crawler.items import MobileItem
from scrapy_redis.spiders import RedisCrawlSpider

mutex = threading.Lock()

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class MobileSpider(RedisCrawlSpider):

    name = "mobile_spider"
    allowed_domains = ["imcaller.com"]
    redis_key = 'mobile_spider:imcaller'

    def __init__(self, mobile_number=None):
        self.mobile_number = mobile_number

    def start_requests(self):
        print 'start_requests'
        if self.mobile_number:
            mobile_number_array = []
            if str(self.mobile_number).find(",") == -1:
                mobile_number_array.append(self.mobile_number)
            else:
                mobile_number_array = str(self.mobile_number).split(',')
            for t_mobile_number in mobile_number_array:
                request = scrapy.Request(
                    url=crypt.get_posturl(),
                    method='POST',
                    body=crypt.get_poststr(t_mobile_number),
                    headers={
                        'X-CLIENT-PFM': '20',
                        'X-CLIENT-VCODE': '81',
                        'X-CLIENT-PID': '8888888',
                        'Content-Type': 'application/json; charset=utf-8',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                        'Accept-Encoding': 'gzip',
                    }
                )
                request.meta['mobile'] = t_mobile_number
                request.meta['msk'] = crypt.sk
                request.meta['mtk'] = crypt.tk
                request.meta['muid'] = crypt.uid
                yield request
        else:
            parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
            file_path = os.path.join(parent_dir, 'mobilecode.txt')
            mobile_number_segments = []
            with open(file_path, 'r') as f:
                line = f.readline()
                while line:
                    mobile_number_segments.append(line.strip())
                    line = f.readline()

            for mobile_number_segments_index in xrange(len(mobile_number_segments)):
                mobile_number_segment = random.choice(mobile_number_segments)
                print 'fetching mobile code : ' + mobile_number_segment
                seed = int(mobile_number_segment) * 10000
                random_num = random.randint(1, 9)
                for i in xrange(10000):
                    mobile_number = seed + random_num * 1111 - i
                    request = scrapy.Request(
                        url=crypt.get_posturl(),
                        method='POST',
                        body=crypt.get_poststr(str(mobile_number)),
                        headers={
                            'X-CLIENT-PFM': '20',
                            'X-CLIENT-VCODE': '81',
                            'X-CLIENT-PID': '8888888',
                            'Content-Type': 'application/json; charset=utf-8',
                            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                            'Accept-Encoding': 'gzip',
                        }
                    )
                    request.meta['mobile'] = str(mobile_number)
                    request.meta['msk'] = crypt.sk
                    request.meta['mtk'] = crypt.tk
                    request.meta['muid'] = crypt.uid
                    yield request

    def parse(self, response):
        try:
            json_obj = json.loads(response.body)
            if str(json_obj['resultCode'] == 0):
                json_str = crypt.decrypt_mobile_sk(json_obj['data'], str(response.request.meta['msk']))
                print json_str
                data = json.loads(json_str)
                # if str(data['n']) != '':
                item = MobileItem()
                item['jsonstr'] = json_str
                item['name'] = str(data['n'])
                item['mobile'] = str(data['p'])
                item['timestamp'] = int(time.time() * 300)
                item['_id'] = crypt.get_md5(str(data['p']))
                yield item
            elif str(json_obj['resultCode']) == '-1':
                print 'result code : -1'
                print 'response body: ' + str(response.body)
                print 'uid: ' + str(crypt.uid) + ' tk: ' + str(crypt.tk) + ' sk: ' + str(crypt.sk)
            else:
                if response.request.meta['sk'] == crypt.sk:
                    # sendEmail("change auth")
                    if mutex.acquire(10):
                        if not crypt.is_changing:
                            print 'changing auth'
                            if crypt.change_auth():
                                print 'change auth success'
                            else:
                                print 'change auth failure'
                        else:
                            while crypt.is_changing:
                                time.sleep(1)
                        mutex.release()

                request = scrapy.Request(
                    url=crypt.get_posturl(),
                    method='POST',
                    body=crypt.get_poststr(response.request.meta['mobile']),
                    headers={
                        'X-CLIENT-PFM': '20',
                        'X-CLIENT-VCODE': '81',
                        'X-CLIENT-PID': '8888888',
                        'Content-Type': 'application/json; charset=utf-8',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                        'Accept-Encoding': 'gzip',
                    }
                )
                request.meta['mobile'] = response.request.meta['mobile']
                request.meta['msk'] = crypt.sk
                request.meta['mtk'] = crypt.tk
                request.meta['muid'] = crypt.uid
                yield request
                # '{"resultCode":1400,"errorMsg":"req invalid"}'
                print json_obj['resultCode']
                print json_obj['errorMsg']
        except Exception, e:
            print e.message
            print traceback.format_exc()

    def start_single_requests(self):
        request = scrapy.Request(
            url=crypt.get_posturl(),
            method='POST',
            body=crypt.get_poststr(self.mobile_number),
            headers={
                'X-CLIENT-PFM': '20',
                'X-CLIENT-VCODE': '81',
                'X-CLIENT-PID': '8888888',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                'Accept-Encoding': 'gzip',
            }
        )
        request.meta['mobile'] = self.mobile_number
        request.meta['msk'] = crypt.sk
        request.meta['mtk'] = crypt.tk
        request.meta['muid'] = crypt.uid
        yield request

    def start_random_requests(self):
        print 'start_requests'
        parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
        file_path = os.path.join(parent_dir, 'mobilecode.txt')
        mobile_number_segments = []
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                mobile_number_segments.append(line.strip())
                line = f.readline()

        for mobile_number_segments_index in xrange(len(mobile_number_segments)):
            mobile_number_segment = random.choice(mobile_number_segments)
            print 'fetching mobile code : ' + mobile_number_segment
            seed = int(mobile_number_segment) * 10000
            for i in xrange(10000):
                mobile_number = seed + i
                request = scrapy.Request(
                    url=crypt.get_posturl(),
                    method='POST',
                    body=crypt.get_poststr(str(mobile_number)),
                    headers={
                        'X-CLIENT-PFM': '20',
                        'X-CLIENT-VCODE': '81',
                        'X-CLIENT-PID': '8888888',
                        'Content-Type': 'application/json; charset=utf-8',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                        'Accept-Encoding': 'gzip',
                    }
                )
                request.meta['mobile'] = str(mobile_number)
                request.meta['msk'] = crypt.sk
                request.meta['mtk'] = crypt.tk
                request.meta['muid'] = crypt.uid
                yield request

    def start_sequence_requests(self):
        print 'start_requests'
        parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
        file_path = os.path.join(parent_dir, 'mobilecode.txt')
        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                print 'fetching mobile code : ' + line.strip()
                seed = int(line.strip()) * 10000
                for i in xrange(10000):
                    mobile_number = seed + i
                    request = scrapy.Request(
                        url=crypt.get_posturl(),
                        method='POST',
                        body=crypt.get_poststr(str(mobile_number)),
                        headers={
                            'X-CLIENT-PFM': '20',
                            'X-CLIENT-VCODE': '81',
                            'X-CLIENT-PID': '8888888',
                            'Content-Type': 'application/json; charset=utf-8',
                            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                            'Accept-Encoding': 'gzip',
                        }
                    )
                    request.meta['mobile'] = str(mobile_number)
                    request.meta['msk'] = crypt.sk
                    request.meta['mtk'] = crypt.tk
                    request.meta['muid'] = crypt.uid
                    yield request
                line = f.readline()
