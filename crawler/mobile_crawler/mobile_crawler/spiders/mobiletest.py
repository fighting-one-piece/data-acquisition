#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import random
import uuid
import json
import traceback
from mobile_crawler.spiders.mobilecrypt import crypt

try:
    url = 'http://address.imcaller.com/wp/woa/v1/device.json'
    imei = random.randint(100000000000000, 999999999999999)
    did = str(uuid.uuid1()).replace('-', '')[0:16]
    data = '{"pfm":"android","imei":"' + str(imei) + '","pid":"8888888","did":"' + did + '","vcode":81}'
    postStr = "{\"data\":\"" + crypt.encrypt_register(data) + "\"}"
    req_header = {
        'X-CLIENT-PFM': '20',
        'X-CLIENT-VCODE': '81',
        'X-CLIENT-PID': '8888888',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
        'Accept-Encoding': 'gzip',
    }
    req_timeout = 50
    req = urllib2.Request(url=url, headers=req_header, data=postStr)
    resp = urllib2.urlopen(req, None, req_timeout)
    html = resp.read()
    jsonobj = json.loads(html)
    print jsonobj
    if str(jsonobj['resultCode']) != '0':
        print 'False'
    else:
        jsonobj = json.loads(crypt.decrypt_register(json.loads(html)["data"]))
        crypt.uid = jsonobj['uid']
        crypt.sk = jsonobj['sk']
        crypt.tk = jsonobj['tk']
        print jsonobj['uid']
        print jsonobj['sk']
        print jsonobj['tk']
        print 'True'
except Exception, e:
    print e.message
    print traceback.format_exc()