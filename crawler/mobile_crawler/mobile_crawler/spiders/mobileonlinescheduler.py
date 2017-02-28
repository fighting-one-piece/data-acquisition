# -*- coding:utf-8 -*-

import os
import sys
import six
import time
import redis
import scrapy
import cPickle as pickle
from mobilecrypt import crypt

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def loads(s):
    return pickle.loads(s)

def dumps(obj):
    return pickle.dumps(obj, protocol=-1)

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
    cb = request.callback
    eb = request.errback
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': cb,
        'errback': eb,
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

def _find_method(obj, func):
    if obj:
        try:
            func_self = six.get_method_self(func)
        except AttributeError:  # func has no __self__
            pass
        else:
            if func_self is obj:
                return six.get_method_function(func).__name__
    raise ValueError("Function %s is not a method of: %s" % (func, obj))


def _get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        raise ValueError("Method %r not found in: %s" % (name, obj))

def _encode_request(request):
    """Encode a request object"""
    obj = request_to_dict(request)
    return dumps(obj)

def pushQueue(mobile_number):
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

    redis_client = redis.Redis(host='192.168.0.21', port=6379)
    redis_client.zadd('mobile_online_spider:requests', _encode_request(request), 1.0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'parameter is not null'
    mobile_number_string = str(sys.argv[1]).strip()
    mobile_number_array = []
    if mobile_number_string.find(",") == -1:
        mobile_number_array.append(mobile_number_string)
    else:
        mobile_number_array = mobile_number_string.split(',')
    for mobile_number in mobile_number_array:
        pushQueue(mobile_number)
