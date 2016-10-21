# -*- coding: utf-8 -*-

import os
import sys
import json
import redis
import random
import requests
import platform
import threading
from bs4 import BeautifulSoup
from selenium import webdriver

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

def static_crawl_proxy360_proxies():
    redis_client = redis.Redis(host='192.168.0.21', port=6379)
    proxies_data = redis_client.get('VOTE_STATIC_PROXIES')
    if proxies_data:
        proxies = json.loads(proxies_data)
    else:
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
                    proxy['http'] = 'http://' + ip_port
                    proxy['https'] = 'http://' + ip_port
                    proxies.append(proxy)
                    ip_port = ''
        redis_client.set('VOTE_STATIC_PROXIES', json.dumps(proxies), 300)
    return proxies

def static_crawl_kuaidaili_proxies():
    redis_client = redis.Redis(host='192.168.0.21', port=6379)
    proxies_data = redis_client.get('STATIC_1_PROXIES')
    if proxies_data:
        proxies = json.loads(proxies_data)
    else:
        proxies = []
        url = 'http://www.kuaidaili.com/free/inha/'
        for i in xrange(21):
            response = requests.get(url + str(i))
            html = BeautifulSoup(response.text, 'html.parser')
            tr_tags = html.select('table.table tbody tr')
            for tr_tag in tr_tags:
                td_tags = tr_tag.select('td')
                proxy = {}
                for td_tag in td_tags:
                    if td_tag.has_attr('data-title'):
                        data_title = td_tag.get('data-title')
                        if data_title == 'IP':
                            ip = td_tag.string.strip()
                        elif data_title == 'PORT':
                            port = td_tag.string.strip()
                proxy['http'] = 'http://' + ip + ":" + port
                proxy['https'] = 'http://' + ip + ":" + port
                proxies.append(proxy)
        redis_client.set('STATIC_1_PROXIES', json.dumps(proxies), 300)
    return proxies

proxies_set = set()

def dynamic_crawl_goubanjia_proxies():
    # redis_client = redis.Redis(host='192.168.0.21', port=6379)
    # proxies_data = redis_client.get('VOTE_DYNAMIC_PROXIES')
    # if proxies_data:
    #     proxies = json.loads(proxies_data)
    # else:
    #     order_id = 'a66cff43be83d8f1c3724945ded69549'
    #     url = 'http://dynamic.goubanjia.com/dynamic/get/' + order_id + '.html?ttl'
    #     response = requests.get(url)
    #     datas = str(response.text).split(',')
    #     proxies = {}
    #     proxies['http'] = 'http://' + str(datas[0]).strip()
    #     proxies['https'] = 'http://' + str(datas[0]).strip()
    #     redis_client.set('VOTE_DYNAMIC_PROXIES', json.dumps(proxies), int(datas[1]) / 1000)
    #     print proxies
    # return proxies
    order_id = 'a66cff43be83d8f1c3724945ded69549'
    url = 'http://dynamic.goubanjia.com/dynamic/get/' + order_id + '.html?ttl'
    response = requests.get(url)
    datas = str(response.text).split(',')
    ip_port = str(datas[0]).strip()
    while ip_port in proxies_set:
        response = requests.get(url)
        datas = str(response.text).split(',')
        ip_port = str(datas[0]).strip()
    proxies_set.add(ip_port)
    proxies = {}
    proxies['http'] = 'http://' + ip_port
    proxies['https'] = 'http://' + ip_port
    return proxies

def selenium_crawl_goubanjia_proxies():
    redis_client = redis.Redis(host='192.168.0.21', port=6379)
    proxies_data = redis_client.get('VOTE_SELENIUM_DYNAMIC_PROXIES')
    if proxies_data:
        proxies = json.loads(proxies_data)
    else:
        parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
        parent_dir = os.path.split(parent_dir)[0]
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
            proxy['http'] = 'http://' + ips[i] + ':' + ports[i]
            proxy['https'] = 'http://' + ips[i] + ':' + ports[i]
            proxies.append(proxy)
        browser.close()
        browser.quit()
        redis_client.set('VOTE_SELENIUM_DYNAMIC_PROXIES', json.dumps(proxies), 300)
    return proxies

def selenium_crawl_xicidaili_proxies():
    parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    parent_dir = os.path.split(parent_dir)[0]
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
    for i in xrange(6):
        target_url = "http://www.xicidaili.com/nt/" + str(i)
        browser.get(target_url)
        tr_elements = browser.find_elements_by_css_selector('tr.odd')
        for tr_element in tr_elements:
            datas = str(tr_element.text).split(' ')
            proxy = {}
            proxy['http'] = 'http://' + datas[0] + ':' + datas[1]
            proxy['https'] = 'http://' + datas[0] + ':' + datas[1]
            proxies.append(proxy)

    browser.close()
    browser.quit()
    return proxies

def vote(proxies):
    url = 'http://top.chengdu.cn/acts/2016_gdwh/base.php'
    data = {"action": "vote", "tid": "35375387"}
    print proxies
    try:
        hit = 0
        for i in xrange(100):
            headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'top.chengdu.cn',
                    'Cookie': '',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': random.choice(USER_AGENTS),
                    'Referer': 'http://top.chengdu.cn/acts/2016_gdwh/?pageNo=51&kwd='}
            response = requests.post(url, data=data, verify=False, headers=headers, proxies=proxies)
            if response.text == '({msg:\'每个IP在24小时之内，只能投票100次。\'})':
                hit = hit + 1
                print '%s hit %s' % (response.text, hit)
                if hit == 10:
                    break

    except Exception, e:
        print e.message

class refresh_vote_action(threading.Thread):

    def __init__(self, thread_id):
        super(refresh_vote_action, self).__init__()
        self.thread_id = thread_id

    def run(self):
        proxies_array = selenium_crawl_goubanjia_proxies()
        proxies_0 = selenium_crawl_xicidaili_proxies()
        proxies_1 = static_crawl_proxy360_proxies()
        # proxies_2 = static_crawl_kuaidaili_proxies()
        proxies_array.extend(proxies_0)
        proxies_array.extend(proxies_1)
        # proxies_array.extend(proxies_2)
        for i in xrange(20):
            if i % 5 == 0:
                proxies_array.append(dynamic_crawl_goubanjia_proxies())
            print 'thread %s start running in %s ' % (self.thread_id, i)
            vote(random.choice(proxies_array))
            # vote(dynamic_crawl_goubanjia_proxies())

if __name__ == '__main__':
    while True:
        thread_pool = []
        for i in xrange(5):
            thread_pool.append(refresh_vote_action(i))

        for t_thread in thread_pool:
            t_thread.start()

        for t_thread in thread_pool:
            t_thread.join()

        print 'run finish'

