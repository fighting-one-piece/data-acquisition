# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import redis
import random
import base64
import requests
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from settings import REDIS_HOST, REDIS_PORT

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class UserAgentMiddleware(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        user_agent = random.choice(self.agents)
        print "**********User-Agent: " + user_agent
        request.headers.setdefault('User-Agent', user_agent)

class QueueProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def process_request(self, request, spider):

        proxies_data = self.redis_client.get('QUEUE_PROXIES')
        if proxies_data:
            proxies = json.loads(proxies_data)
        else:
            proxies = []
            proxies_queue = self.redis_client.zrange('proxy_id_queue', 0, 200)
            for ip_port in proxies_queue:
                proxy = {}
                proxy['ip_port'] = str(ip_port).strip().replace(' ', '')
                proxy['user_pass'] = ''
                proxies.append(proxy)
            self.redis_client.set('QUEUE_PROXIES', json.dumps(proxies), 180)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************QueueProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************QueueProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class StaticProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def process_request(self, request, spider):

        proxies_data = self.redis_client.get('STATIC_PROXIES')
        if proxies_data:
            proxies = json.loads(proxies_data)
        else:
            proxies = []
            proxies_01 = static_crawl_proxy360_proxy_ip()
            proxies_02 = static_crawl_xicidaili_proxy_ip()
            proxies.extend(proxies_01)
            proxies.extend(proxies_02)
            self.redis_client.set('STATIC_PROXIES', json.dumps(proxies), 600)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**********StaticProxyMiddleware have pass**********" + proxy['ip_port']
        else:
            print "**********StaticProxyMiddleware no pass**********" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class DynamicProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def process_request(self, request, spider):

        proxies_data = self.redis_client.get('DYNAMIC_PROXIES')
        if proxies_data:
            proxies = json.loads(proxies_data)
        else:
            proxies = dynamic_crawl_goubanjia_proxy_ip()
            self.redis_client.set('DYNAMIC_PROXIES', json.dumps(proxies), 60)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**********DynamicProxyMiddleware have pass**********" + proxy['ip_port']
        else:
            print "**********DynamicProxyMiddleware no pass**********" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class SeleniumProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def process_request(self, request, spider):

        proxies_data = self.redis_client.get('SELENIUM_PROXIES')
        if proxies_data:
            proxies = json.loads(proxies_data)
        else:
            proxies = []
            goubanjia_proxies = selenium_crawl_goubanjia_proxy_ip()
            proxies.extend(goubanjia_proxies)
            # xicidaili_proxies = selenium_crawl_xicidaili_proxy_ip()
            # proxies.extend(xicidaili_proxies)
            self.redis_client.set('SELENIUM_PROXIES', json.dumps(proxies), 300)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**********SeleniumProxyMiddleware have pass**********" + proxy['ip_port']
        else:
            print "**********SeleniumProxyMiddleware no pass**********" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class SeleniumOptProxyMiddleware(object):

    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.browser = selenium_brower_startup()

    def process_request(self, request, spider):

        proxies_data = self.redis_client.get('SELENIUM_PROXIES')
        if proxies_data:
            proxies = json.loads(proxies_data)
        else:
            proxies = []
            goubanjia_proxies = selenium_opt_crawl_goubanjia_proxy_ip(self.browser)
            proxies.extend(goubanjia_proxies)
            xicidaili_proxies = selenium_opt_crawl_xicidaili_proxy_ip(self.browser)
            proxies.extend(xicidaili_proxies)
            self.redis_client.set('SELENIUM_PROXIES', json.dumps(proxies), 300)

        proxy = random.choice(proxies)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**********SeleniumProxyMiddleware have pass**********" + proxy['ip_port']
        else:
            print "**********SeleniumProxyMiddleware no pass**********" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

    def __del__(self):
        del self.redis_client
        selenium_brower_stop(self.browser)

def static_crawl_proxy360_proxy_ip():
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

def static_crawl_xicidaili_proxy_ip():
    url = 'http://api.xicidaili.com/free2016.txt'
    response = requests.get(url)
    pattern = '(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}):(\\d+)'
    ip_port_array = re.findall(pattern, response.text)
    proxies = []
    for ip_port in ip_port_array:
        proxy = {}
        proxy['ip_port'] = ip_port[0] + ':' + ip_port[1]
        proxy['user_pass'] = ''
        proxies.append(proxy)
    return proxies

def static_crawl_goubanjia_proxy_id():
    url = 'http://www.goubanjia.com/'
    req_session = requests.session()
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.baidu.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }
    response = req_session.get(url, headers=headers)
    html = BeautifulSoup(response.text, 'html.parser')
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

def dynamic_crawl_goubanjia_proxy_ip():
    proxies = []
    ips = set()
    order_id = 'a66cff43be83d8f1c3724945ded69549'
    for i in xrange(100):
        url = 'http://dynamic.goubanjia.com/dynamic/get/' + order_id + '.html?ttl'
        response = requests.get(url)
        datas = str(response.text).split(':')
        port_time = datas[1].split(',')
        if datas[0] not in ips:
            ips.add(datas[0])
            proxy = {}
            proxy['ip_port'] = datas[0] + ':' + port_time[0].strip()
            proxy['user_pass'] = ''
            proxies.append(proxy)
    return proxies

def selenium_brower_startup():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path

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
    return browser

def selenium_brower_stop(browser):
    browser.close()
    browser.quit()

def selenium_opt_crawl_goubanjia_proxy_ip(browser):
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
    return proxies

def selenium_opt_crawl_xicidaili_proxy_ip(browser):
    proxies = []
    for i in xrange(11):
        target_url = "http://www.xicidaili.com/nt/" + str(i)
        browser.get(target_url)
        tr_elements = browser.find_elements_by_css_selector('tr.odd')
        for tr_element in tr_elements:
            datas = str(tr_element.text).split(' ')
            proxy = {}
            proxy['ip_port'] = datas[0] + ':' + datas[1]
            proxy['user_pass'] = ''
            proxies.append(proxy)
    return proxies

def selenium_crawl_goubanjia_proxy_ip():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path

    chrome_driver = os.path.abspath(driver_file_path)
    os.environ['webdriver.chrome.driver'] = chrome_driver

    if current_operation_system == 'Windows':
        browser = webdriver.Chrome(chrome_driver)
    elif current_operation_system == 'Linux':
        service_log_path = "{}/chromedriver.log".format(chrome_driver)
        service_args = ['--verbose']
        browser = webdriver.Chrome(chrome_driver, service_args=service_args, service_log_path=service_log_path)

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
    return proxies

def selenium_crawl_xicidaili_proxy_ip():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path

    chrome_driver = os.path.abspath(driver_file_path)
    os.environ['webdriver.chrome.driver'] = chrome_driver

    if current_operation_system == 'Windows':
        browser = webdriver.Chrome(chrome_driver)
    elif current_operation_system == 'Linux':
        service_log_path = "{}/chromedriver.log".format(chrome_driver)
        service_args = ['--verbose']
        browser = webdriver.Chrome(chrome_driver, service_args=service_args, service_log_path=service_log_path)

    proxies = []
    for i in xrange(11):
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
    return proxies

if __name__ == '__main__':
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    elif current_operation_system == 'Linux':
        driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    print driver_file_path
    print static_crawl_goubanjia_proxy_id()
