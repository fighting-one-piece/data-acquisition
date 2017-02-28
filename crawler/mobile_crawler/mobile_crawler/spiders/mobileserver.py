# -*- coding:utf-8 -*-

import sys
import json
from mobileonlineparser import parseMobile
from wsgiref.simple_server import make_server

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def application(environ, start_response):
    request_url = environ['PATH_INFO'][1:]
    values = str(request_url).strip().split('/')
    print values
    mobile = values[2]

    status = '200 OK'
    body = json.dumps(parseMobile(mobile))

    start_response(status, [('Content-Type', 'application/json')])

    return [body.encode('utf-8')]

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('192.168.0.198', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
