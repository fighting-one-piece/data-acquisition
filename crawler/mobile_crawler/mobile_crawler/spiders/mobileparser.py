# -*- coding:utf-8 -*-

import sys
import six
import json
import scrapy
import traceback
import pymongo
import cPickle as pickle
from mobilecrypt import crypt
from twisted.internet import reactor
from http10 import HTTP10DownloadHandler
from http11 import HTTP11DownloadHandler
from scrapy.utils.project import get_project_settings

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of a bytes object `text`. If `text`
    is already an unicode object, return it as-is."""
    if isinstance(text, six.text_type):
        return text
    if not isinstance(text, (bytes, six.text_type)):
        raise TypeError('to_unicode must receive a bytes, str or unicode '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.decode(encoding, errors)

def request_to_dict(request):
    """Convert Request object to a dict.
    If a spider is given, it will try to find out the name of the spider method
    used in the callback and store that as the callback.
    """
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': request.callback,
        'errback': request.errback,
        'method': request.method,
        'headers': dict(request.headers),
        'body': request.body,
        'cookies': request.cookies,
        'meta': request.meta,
        '_encoding': request._encoding,
        'priority': request.priority,
        'dont_filter': request.dont_filter,
    }
    return d

def _encode_request(request):
    """Encode a request object"""
    obj = request_to_dict(request)
    return pickle.dumps(obj, protocol=-1)

def http10handle(self, request):
    downloader = HTTP10DownloadHandler()
    deferred = downloader.download_request(request)
    deferred.addCallback(self.parseResponse)
    reactor.run()

def fetchData(mobile_number):
    request = scrapy.Request(
        url=crypt.get_posturl(),
        method='POST',
        body=crypt.get_poststr(mobile_number),
        headers={
            'X-CLIENT-PFM': '20',
            'X-CLIENT-VCODE': '81',
            'X-CLIENT-PID': '8888888',
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
            'Accept-Encoding': 'gzip',
        }
    )
    request.meta['mobile'] = mobile_number
    request.meta['msk'] = crypt.sk
    request.meta['mtk'] = crypt.tk
    request.meta['muid'] = crypt.uid

    settings = get_project_settings()
    downloader = HTTP11DownloadHandler(settings)
    deferred = downloader.download_request(request)
    deferred.addCallback(parseResponse, request)
    deferred.addErrback(parseError)
    reactor.run()

def parseResponse(response, request):
    try:
        json_obj = json.loads(response.body)
        if str(json_obj['resultCode'] == 0):
            json_str = crypt.decrypt_mobile_sk(json_obj['data'], str(request.meta['msk']))
            print json_str
            # MongoDBUtils().insertDB(json.loads(json_str))
        elif str(json_obj['resultCode']) == '-1':
            print 'result code : -1'
            print 'response body: ' + str(response.body)
            print 'uid: ' + str(crypt.uid) + ' tk: ' + str(crypt.tk) + ' sk: ' + str(crypt.sk)
    except Exception, e:
        print e.message
        print traceback.format_exc()
    reactor.stop()

def parseError(error):
    print "an error has occurred: <%s>" %str(error)
    reactor.stop()


def parseMobile(mobile_number_string):
    mobile_number_array = []
    if mobile_number_string.find(",") == -1:
        mobile_number_array.append(mobile_number_string)
    else:
        mobile_number_array = mobile_number_string.split(',')
    for mobile_number in mobile_number_array:
        fetchData(mobile_number)

if __name__ == '__main__':
    parseMobile('15809981991')
    # if len(sys.argv) < 2:
    #     print 'parameter is not null'
    # mobile_number_string = str(sys.argv[1]).strip()
    # mobile_number_array = []
    # if mobile_number_string.find(",") == -1:
    #     mobile_number_array.append(mobile_number_string)
    # else:
    #     mobile_number_array = mobile_number_string.split(',')
    # for mobile_number in mobile_number_array:
    #     fetchData(mobile_number)
