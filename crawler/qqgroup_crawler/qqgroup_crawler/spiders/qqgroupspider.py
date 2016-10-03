# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import urllib
import scrapy
from qqgroup_crawler.items import QQGroupItem
from scrapy_redis.spiders import RedisCrawlSpider

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class QQGroupSpider(RedisCrawlSpider):

    name = "qqgroup_spider"
    allowed_domains = ["qq.com"]
    redis_key = 'qqgroup_spider:qqgroup'

    def parse(self, response):
        json_obj = json.loads(response.body)
        error_code = json_obj['ec']
        if error_code == 0:
            group_list = json_obj['gList']
            for group in group_list:
                qq_group_item = QQGroupItem()
                qq_group_item['_id'] = group['gc']
                qq_group_item['groupCode'] = group['gc']
                qq_group_item['groupFlag'] = group['gFlag']
                qq_group_item['groupLevel'] = group['gLevel']
                qq_group_item['groupMemNum'] = group['gMemNum']
                qq_group_item['groupMaxMem'] = group['gMaxMem']
                qq_group_item['groupOwner'] = group['gOwner']
                qq_group_item['groupName'] = group['gName'].strip()
                qq_group_item['groupIntro'] = group['gIntro'].strip()
                qq_group_item['groupTags'] = group['gTags'].strip()
                qq_group_item['groupClass'] = group['gClass']
                qq_group_item['groupClass2'] = group['gClass2'].strip()
                qq_group_item['groupClassText'] = group['gClassText'].strip()
                yield qq_group_item
            is_end_flag = json_obj['IsEnd']
            if is_end_flag == 1:
                print 'current url pagination has finished!'
            else:
                current_url = response.url
                regex = 'p=\d+'
                matcher = re.compile(regex).search(current_url)
                if matcher:
                    page_string = matcher.group()
                    page_tag = page_string[0:page_string.index('=') + 1]
                    page_num = int(page_string[page_string.index('=') + 1:])
                    new_page_string = page_tag + str(page_num + 1)
                    next_url = current_url.replace(page_string, new_page_string)
                    cookies = response.request.meta['cookies']
                    meta = {'cookiejar': 1, 'cookies': cookies}
                    request = scrapy.Request(
                        url=next_url,
                        method='GET',
                        cookies=cookies,
                        meta=meta
                    )
                    yield request
                else:
                    print 'not match'
        else:
            print json_obj['em']

    def start_requests(self):
        parent_dir = os.path.dirname(__file__)
        zh_file_path = os.path.join(parent_dir, 'qqgroup_zh.txt')
        keywords = []
        with open(zh_file_path, 'r') as f:
            line = f.readline()
            while line:
                keywords.append(line.strip())
                line = f.readline()
        en_file_path = os.path.join(parent_dir, 'qqgroup_en.txt')
        with open(en_file_path, 'r') as f:
            line = f.readline()
            while line:
                keywords.append(line.strip())
                line = f.readline()
        for keyword in keywords:
            url = 'http://qqun.qq.com/cgi-bin/qun_search/search_group?k=%s&p=2&n=8&c=1&t=0&st=1&r=0.8119000566657633&d=1&bkn=825315115&v=0' %(urllib.quote(keyword))
            cookie = 'tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; luin=o0125906088; lskey=0001000037f88ec8f9f9821744d28f594b49cec920d3e6bdf70f23f46dfd1994a0ba6997a3597e1811ce5799; pgv_pvid=512697556; o_cookie=125906088; ptisp=ctc; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0125906088; uin=o0125906088; skey=@vm7DaoTBb'
            cookies = {}
            items = cookie.split(';')
            for item in items:
                kv = item.split('=')
                cookies[kv[0]] = kv[1]
            # cookies = {'Cookie': cookie}
            meta = {'cookiejar': 1, 'cookies': cookies}
            request = scrapy.Request(
                url=url,
                method='GET',
                cookies=cookies,
                meta=meta
            )
            yield request