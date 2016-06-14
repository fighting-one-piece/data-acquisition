# -*- coding:utf-8 -*-
'''
@author: wulin
'''

import threadpool
import random
import time

def hello(self):
    time.sleep(2);
    return "hello";

data = [ random.randint(1, 10) for i in range(20) ]

def print_result(request, result):
    print "the result is %s %r" %(request.requestID, result)

pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(hello, data, print_result)
[pool.putRequest(request) for request in requests]
pool.wait()