# -*- coding:utf-8 -*-

'''
@author: wulin

'''

import requests
from bs4 import BeautifulSoup

url = 'http://www.loldytt.com/Dianshiju/'
response = requests.get(url)
response.encoding = 'gb2312'
responseText = response.text
bs = BeautifulSoup(responseText, 'html.parser', from_encoding='gb2312')

lis = bs.select('div.xifen ul li')
for li in lis:
    pText = li.find('p').text
    a = li.find('a')
    print '%s %s %s' %(pText, a.text, a['href'])

