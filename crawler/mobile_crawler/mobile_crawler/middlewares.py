# -*- coding: utf-8 -*-

import os
import sys
import json
import redis
import random
import base64
import requests
import platform
from settings import PROXIES
from bs4 import BeautifulSoup
from selenium import webdriver
from settings import REDIS_HOST, REDIS_PORT

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class UserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxies = crawl_proxy360_proxy_ip()
        proxy = random.choice(proxies)
        # proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class SeleniumProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def process_request(self, request, spider):

        proxies_str = self.redis_client.get('PROXIES')
        if proxies_str:
            proxies = json.loads(self.redis_client.get('PROXIES'))
        else:
            proxies = []
            goubanjia_proxies = selenium_crawl_goubanjia_proxy_id()
            proxies.extend(goubanjia_proxies)
            xicidaili_proxies = selenium_crawl_xicidaili_proxy_ip()
            proxies.extend(xicidaili_proxies)
            self.redis_client.set('PROXIES', json.dumps(proxies), 300)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

def crawl_proxy_id():
    print ''

def selenium_crawl_goubanjia_proxy_id():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path

    # chrome_driver = os.path.abspath('F:\develop\crawler\chromedriver.exe')
    chrome_driver = os.path.abspath(driver_file_path)
    os.environ['webdriver.chrome.driver'] = chrome_driver

    if current_operation_system == 'Windows':
        browser = webdriver.Chrome(chrome_driver)
    elif current_operation_system == 'Linux':
        service_log_path = "{}/chromedriver.log".format(chrome_driver)
        service_args = ['--verbose']
        browser = webdriver.Chrome(chrome_driver, service_args=service_args, service_log_path=service_log_path)

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

    browser.close()
    browser.quit()
    browser = None

    return proxies

def selenium_crawl_xicidaili_proxy_ip():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path

    # chrome_driver = os.path.abspath('F:\develop\crawler\chromedriver.exe')
    chrome_driver = os.path.abspath(driver_file_path)
    os.environ['webdriver.chrome.driver'] = chrome_driver

    if current_operation_system == 'Windows':
        browser = webdriver.Chrome(chrome_driver)
    elif current_operation_system == 'Linux':
        service_log_path = "{}/chromedriver.log".format(chrome_driver)
        service_args = ['--verbose']
        browser = webdriver.Chrome(chrome_driver, service_args=service_args, service_log_path=service_log_path)

    proxies = []
    for i in xrange(10):
        target_url = "http://www.xicidaili.com/nt/" + str(i)
        browser.get(target_url)
        tr_elements = browser.find_elements_by_css_selector('tr.odd')
        for tr_element in tr_elements:
            datas = str(tr_element.text).split(' ')
            proxy = {}
            proxy['ip_port'] = datas[0] + ':' + datas[1]
            proxy['user_pass'] = ''
            proxies.append(proxy)

    browser.close()
    browser.quit()
    browser = None

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
    return proxies


if __name__ == '__main__':
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path
    selenium_crawl_xicidaili_proxy_ip()