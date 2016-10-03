# -*- coding: utf-8 -*-

import os
import sys
import json
import redis
import random
import requests
import platform
from bs4 import BeautifulSoup
from selenium import webdriver

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def selenium_crawl_proxy_id():
    chrome_driver = os.path.abspath('F:\develop\crawler\chromedriver.exe')
    os.environ['webdriver.chrome.driver'] = chrome_driver
    browser = webdriver.Chrome(chrome_driver)

    # firefoxBin = os.path.abspath(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
    # os.environ["webdriver.firefox.bin"] = firefoxBin
    # browser = webdriver.Firefox()

    # ie_driver = os.path.abspath('IEDriverServer.exe')
    # os.environ["webdriver.ie.driver"] = ie_driver
    # browser = webdriver.Ie(ie_driver)

    browser.get("http://www.goubanjia.com/")
    ips = []
    ip_elements = browser.find_elements_by_css_selector('table.table tr td.ip')
    for ip_element in ip_elements:
        ips.append(ip_element.text)
    ports = []
    port_elements = browser.find_elements_by_css_selector('table.table tr td.port')
    for port_element in port_elements:
        ports.append(port_element.text)
    proxies = []
    for i in xrange(len(ips)):
        proxy = {}
        proxy['ip_port'] = ips[i] + ':' + ports[i]
        proxy['user_pass'] = ''
        proxies.append(proxy)
    print proxies

    browser.close()
    browser.quit()
    browser = None

    # redisCli = redis.Redis(host='192.168.0.21', port=6379)
    # redisCli.set('PROXIES', json.dumps(proxies), 10)
    # print redisCli.keys()
    # PROXIES = json.loads(redisCli.get('PROXIES'))
    # print redisCli.keys()
    # print random.choice(PROXIES)

    return proxies

def crawl_goubanjia_proxy_ip():
    url = 'http://www.goubanjia.com/'
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    # td_tags = html.select('table.table tr td.ip')
    # for td_tag in td_tags:
    #     print td_tag
    #     td_tag_all_tags = td_tag.contents
    #     ip = ''
    #     for td_tag_tag in td_tag_all_tags:
    #         if td_tag_tag.has_attr('style'):
    #             style_name = td_tag_tag.get('style').strip().replace(' ', '')
    #             if style_name and (style_name == 'display:inline-block;'):
    #                 if td_tag_tag.string:
    #                     ip = ip + td_tag_tag.string
    #         else:
    #             if td_tag_tag.string:
    #                 print 'tag: ' + td_tag_tag.string
    #                 ip = ip + td_tag_tag.string
    #     print ip
    proxies = []
    td_tags = html.select('table.table tr td')
    ip_port = ''
    for td_tag in td_tags:
        if td_tag.has_attr('class'):
            class_value = td_tag.get('class')
            if class_value[0] == 'ip':
                td_tag_all_tags = td_tag.contents
                ip = ''
                for td_tag_tag in td_tag_all_tags:
                    if td_tag_tag.has_attr('style'):
                        style_name = td_tag_tag.get('style').strip().replace(' ', '')
                        if style_name and (style_name == 'display:inline-block;'):
                            if td_tag_tag.string:
                                ip = ip + td_tag_tag.string
                    else:
                        if td_tag_tag.string:
                            ip = ip + td_tag_tag.string
                print ip
                ip_port = ip_port + ip
            else:
                print td_tag
                print td_tag.string
                ip_port = ip_port + ':' + td_tag.string
                proxy = {}
                proxy['ip_port'] = ip_port
                proxy['user_pass'] = ''
                proxies.append(proxy)
                ip_port = ''
    print proxies
    td_port_tags = html.select('table.table tr td.port')
    for td_port_tag in td_port_tags:
        print td_port_tag
    print html

def crawl_xicidaili_proxy_ip():
    chrome_driver = os.path.abspath('F:\develop\crawler\chromedriver.exe')
    os.environ['webdriver.chrome.driver'] = chrome_driver
    browser = webdriver.Chrome(chrome_driver)

    browser.get("http://www.xicidaili.com/nt/")
    tr_elements = browser.find_elements_by_css_selector('tr.odd')
    proxies = []
    for tr_element in tr_elements:
        datas = str(tr_element.text).split(' ')
        proxy = {}
        proxy['ip_port'] = datas[0] + ':' + datas[1]
        proxy['user_pass'] = ''
        proxies.append(proxy)

    browser.close()
    browser.quit()
    browser = None

    print proxies
    return proxies

def crawl_proxy360_proxy_ip():
    url = 'http://www.proxy360.cn/default.aspx'
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    ip_port = ''
    span_tags = html.select('div.proxylistitem span.tbBottomLine')
    for span_tag in span_tags:
        if span_tag.has_attr('style'):
            style_value = span_tag.get('style')
            if style_value == 'width:140px;':
                ip_port = ip_port + span_tag.string.strip()
            elif style_value == 'width:50px;':
                ip_port = ip_port + ':' + span_tag.string.strip()
                proxy = {}
                proxy['ip_port'] = ip_port
                proxy['user_pass'] = ''
                proxies.append(proxy)
                ip_port = ''
    print proxies
    return proxies

if __name__ == '__main__':
    operation_system = platform.system()
    if operation_system == 'Windows':
        print 'Windows'
    elif operation_system == 'Linux':
        print 'Linux'
    crawl_xicidaili_proxy_ip()