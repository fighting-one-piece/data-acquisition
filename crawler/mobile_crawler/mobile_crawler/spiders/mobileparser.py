# -*- coding:utf-8 -*-

import sys
import six
import json
import time
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

def encode_request(request):
    """Encode a request object"""
    obj = request_to_dict(request)
    return pickle.dumps(obj, protocol=-1)

def http10handle(self, request):
    downloader = HTTP10DownloadHandler()
    deferred = downloader.download_request(request)
    deferred.addCallback(self.parseResponse)
    reactor.run()

def fetch_mobile_data(mobile_number):
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
    deferred.addCallback(parse_success, request)
    deferred.addErrback(parse_failure)
    reactor.run()

def parse_success(response, request):
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

def parse_failure(error):
    print "an error has occurred: <%s>" %str(error)
    reactor.stop()


def parse_mobile(mobile_number_string):
    mobile_number_array = []
    if mobile_number_string.find(",") == -1:
        mobile_number_array.append(mobile_number_string)
    else:
        mobile_number_array = mobile_number_string.split(',')
    for mobile_number in mobile_number_array:
        fetch_mobile_data(mobile_number)


class MongoDBUtils(object):

    client = None

    def __init__(self):
        self.db = MongoDBUtils.getDBConnection()

    @staticmethod
    def getDBConnection():
        if MongoDBUtils.client is None:
            client = pymongo.MongoClient(host='192.168.0.20', port=27018)
        return client['mobile']


    def insert_db(self, jsonObj):
        try:
            dbitem = self.db['imcaller'].find_one({'mobile': jsonObj['p'], 'name': ''})
            if dbitem:
                if jsonObj['n'] and jsonObj['n'] != '':
                    self.db['imcaller'].update_one({'mobile': jsonObj['p']}, {'$set': {'name': jsonObj['n']}})
            else:
                dbObj = {}
                dbObj['jsonstr'] = json.dumps(jsonObj)
                dbObj['name'] = str(jsonObj['n'])
                dbObj['mobile'] = str(jsonObj['p'])
                dbObj['timestamp'] = int(time.time() * 300)
                dbObj['_id'] = crypt.get_md5(str(jsonObj['p']))
                self.db['imcaller'].insert(dbObj)
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception, e:
            print e.message
            print traceback.format_exc()

    def read_one_from_db(self, mobile):
        try:
            dbitem = self.db['imcaller'].find_one({'mobile': mobile})
            return dbitem
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception, e:
            print e.message
            print traceback.format_exc()


class Parser(object):

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

    def request_to_dict(self, request):
        """Convert Request object to a dict.
        If a spider is given, it will try to find out the name of the spider method
        used in the callback and store that as the callback.
        """
        d = {
            'url': self.to_unicode(request.url),  # urls should be safe (safe_string_url)
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

    def encode_request(self, request):
        """Encode a request object"""
        obj = self.request_to_dict(request)
        return pickle.dumps(obj, protocol=-1)

    def fetch_mobile_data(self, mobile_number):
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
        deferred.addCallback(self.parse_success, request)
        deferred.addErrback(self.parse_failure)
        reactor.run()

    def parse_success(self, response, request):
        print response
        print response.body
        try:
            json_obj = json.loads(response.body)
            if str(json_obj['resultCode'] == 0):
                json_str = crypt.decrypt_mobile_sk(json_obj['data'], str(request.meta['msk']))
                MongoDBUtils().insert_db(json.loads(json_str))
            elif str(json_obj['resultCode']) == '-1':
                print 'result code : -1'
                print 'response body: ' + str(response.body)
                print 'uid: ' + str(crypt.uid) + ' tk: ' + str(crypt.tk) + ' sk: ' + str(crypt.sk)
        except Exception, e:
            print e.message
            print traceback.format_exc()
        reactor.stop()

    def parse_failure(self, error):
        print "an error has occurred: <%s>" % str(error)
        reactor.stop()

    def parse_mobile(self, mobile_number_string):
        mobile_number_array = []
        if mobile_number_string.find(",") == -1:
            mobile_number_array.append(mobile_number_string)
        else:
            mobile_number_array = mobile_number_string.split(',')
        return_result_array = []
        for mobile_number in mobile_number_array:
            item = MongoDBUtils().read_one_from_db(mobile_number)
            if not item:
                self.fetch_mobile_data(mobile_number)
                item = MongoDBUtils().read_one_from_db(mobile_number)
            # item['_id'] = ''
            return_result_array.append(item)
        return return_result_array

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'parameter is not null'
    print Parser().parse_mobile(sys.argv[1])
