# -*- coding:utf-8 -*-

'''
@author: wulin
'''

import re

name = u"2009年11月中国不锈钢丸产品生产销售企业名录207条(更多数据请联系QQ-351729096).xls"

total = 0
ns = []
for n in name:
    print n
    if re.compile(u"[\u4e00-\u9fa5]").match(n) :
        total = total + 3
    else :
        total = total + 1
    ns.append(n)
print total
ns.reverse()
print ''.join(ns)
for arr in ns :
    print str(arr)
    
ss = [1, 2, 3]
print ss[0:len(ss)]

'''
reg = re.compile(u"[\u4e00-\u9fa5]")
m = reg.search(name)
print m.group()
zhs = re.findall(u"[\u4e00-\u9fa5]", name)
for zh in zhs:
    print zh

ens = re.findall(u"[0-9a-zA-Z]", name)
for en in ens:
    print en
'''


