# -*- coding: utf-8 -*-

import re
import urllib
import requests


def genbkn(self, skey):
    b = 5381
    for i in xrange(0, len(skey)):
        b += (b << 5) + ord(skey[i])
    bkn = (b & 2147483647)
    return str(bkn)

def gengtk(self, skey):
    b = 5381
    for i in xrange(0, len(skey)):
        b += (b << 5) + ord(skey[i])
    gtk = (b & 0x7fffffff)
    return str(gtk)

if __name__ == '__main__':
    cookies = {}
    cookie = 'tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; luin=o0125906088; lskey=0001000037f88ec8f9f9821744d28f594b49cec920d3e6bdf70f23f46dfd1994a0ba6997a3597e1811ce5799; pgv_pvid=512697556; o_cookie=125906088; ptisp=ctc; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0125906088; uin=o0125906088; skey=@vm7DaoTBb'
    items = cookie.split(';')
    for item in items:
        kv = item.split('=')
        cookies[kv[0]] = kv[1]
    print cookies

    kw = 'Tecent'
    url = 'http://qqun.qq.com/cgi-bin/qun_search/search_group?k=%s&p=1&n=8&c=1&t=0&st=1&r=0.8119000566657633&d=1&bkn=825315115&v=0' %(urllib.quote(kw))
    cookie = 'tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; luin=o0125906088; lskey=0001000037f88ec8f9f9821744d28f594b49cec920d3e6bdf70f23f46dfd1994a0ba6997a3597e1811ce5799; pgv_pvid=512697556; o_cookie=125906088; ptisp=ctc; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0125906088; uin=o0125906088; skey=@vm7DaoTBb'
    cookies = {'Cookie': cookie}
    resp = requests.get(url, cookies=cookies)
    print resp.text
    result = resp.json()
    IsEnd = result.get('IsEnd')
    print IsEnd
    gList = result.get('gList')
    for item in gList:
        print item

    regex = 'p=\d+'
    matcher = re.compile(regex).search(url)
    if matcher:
        page_string = matcher.group()
        page_tag = page_string[0:page_string.index('=')+1]
        page_num = int(page_string[page_string.index('=') + 1:])
        print page_tag
        print page_num
        new_page_string = page_tag + str(page_num + 1)
        print url.replace(page_string, new_page_string)
    else:
        print 'not match'
