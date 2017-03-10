#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import random
import uuid
import json
import traceback
from mobile_crawler.spiders.mobilecrypt import crypt

def imcaller_call():
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


from twisted.internet import reactor, defer


class HeadlineRetriever(object):
    def processHeadline(self, headline):
        if len(headline) > 50:
            self.d.errback(Exception("The headline ``%s'' is too long!" % (headline,)))
        else:
            self.d.callback(headline)

    def _toHTML(self, result):
        return "<h1>%s</h1>" % (result,)

    def getHeadline(self, input):
        self.d = defer.Deferred()
        reactor.callLater(1, self.processHeadline, input)
        self.d.addCallback(self._toHTML)
        return self.d


def printData(result):
    print result
    # reactor.stop()


def printError(failure):
    print failure
    # reactor.stop()


# h = HeadlineRetriever()
# d = h.getHeadline("Breaking News1: Twisted Takes us to the Moon!")
# d.addCallbacks(printData, printError)
#
# h = HeadlineRetriever()
# d = h.getHeadline("Breaking News2: Twisted Takes us to the Moon!")
# d.addCallbacks(printData, printError)
#
# h = HeadlineRetriever()
# d = h.getHeadline("Breaking News3: Twisted Takes us to the Moon!")
# d.addCallbacks(printData, printError)
#
# h = HeadlineRetriever()
# d = h.getHeadline("Breaking News4: Twisted Takes us to the Moon!")
# d.addCallbacks(printData, printError)
#
# reactor.run()