# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import platform
from mobilecrypt import crypt
from bs4 import BeautifulSoup
from requests import Request, Session
from selenium import webdriver

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def fetch_mobile_number(mobile_number):
    print 'fetch mobile number: ' + mobile_number
    url = crypt.get_posturl()
    data = crypt.get_poststr(mobile_number)
    headers = {
        'X-CLIENT-PFM': '20',
        'X-CLIENT-VCODE': '81',
        'X-CLIENT-PID': '8888888',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
        'Accept-Encoding': 'gzip',
    }
    meta = {"mobile": mobile_number, "msk": crypt.sk, "mtk": crypt.tk, "muid": crypt.uid}
    response = requests.post(url, data, headers=headers)
    print response
    print response.content

def fetch_mobile_number_by_proxyip(mobile_number):
    session = Session()
    url = crypt.get_posturl()
    data = crypt.get_poststr(mobile_number)
    headers = {
        'X-CLIENT-PFM': '20',
        'X-CLIENT-VCODE': '81',
        'X-CLIENT-PID': '8888888',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
        'Accept-Encoding': 'gzip',
    }
    req = Request('POST', url, data=data, headers=headers)
    prepare_request = req.prepare()

    # do something with prepareReq.body
    # prepareReq.body = 'No, I want exactly this as the body.'

    # do something with prepareReq.headers
    # del prepareReq.headers['Content-Type']

    # resp = s.send(prepareReq,
    #               stream=stream,
    #               verify=verify,
    #               proxies=proxies,
    #               cert=cert,
    #               timeout=timeout
    #               )

    # proxies = ["http://45.32.108.74:8080"]

    # proxies = {
    #     'http': 'http://45.32.108.74:8080',
    #     'http': 'http://61.231.188.203:8080',
    #     'http': 'http://101.254.188.198:8080',
    #     'http': 'http://61.160.212.74:3128',
    #     'http': 'http://60.206.148.135:3128',
    # }


    for i in xrange(10):
        try:
            proxies = selenium_crawl_proxy_id()
            resp = session.send(prepare_request, proxies=proxies)
            print resp
        except requests.exceptions.ProxyError, pe:
            print pe.message


def selenium_crawl_proxy_id():
    # parent_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    current_operation_system = platform.system()
    # if current_operation_system == 'Windows':
    #     driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver.exe')
    # elif current_operation_system == 'Linux':
    #     driver_file_path = os.path.join(parent_dir, 'driver', 'chromedriver')
    # print driver_file_path

    chrome_driver = os.path.abspath('F:\develop\crawler\chromedriver.exe')
    # chrome_driver = os.path.abspath(driver_file_path)
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
    proxies = {}
    for i in xrange(len(ips)):
        proxies['http'] = 'http://' + ips[i] + ':' + ports[i]
        break
    print proxies

    browser.close()
    browser.quit()
    browser = None

    return proxies

def fetch_weibo():
    url = 'http://m.weibo.cn/index/feed?format=cards'
    cookie = '_T_WM=c0a201ef32a2aa921133651ce8c4f7db; WEIBOCN_WM=3349; H5_wentry=H5; backURL=http%3A%2F%2Fm.weibo.cn%2F; SUB=_2A2567JwcDeTxGeVH7VUY8S3KyTqIHXVWLiRUrDV6PUJbkdBeLWKjkW0MnEpsejoYM2HaVzW2s6An65iX7g..; SUHB=08JrTsKLs-V7M3; SCF=Ag-4BDFzlevT8zA-LAsNZimZInFvfUn-pNnqdn1bPsvHYgQmMR7wc-TtqbCb833Nn_dyHUHEvdehtoEFRCb3BO8.; SSOLoginState=1474882636; H5_INDEX=0_all; H5_INDEX_TITLE=%E8%A6%8B%E5%88%9D%E5%A6%82%E5%8F%AA%E8%8B%A5%E7%94%9F%E4%BB%8A; M_WEIBOCN_PARAMS=uicode%3D20000174'
    cookies = {'Cookie': cookie}
    resp = requests.get(url, cookies=cookies)
    print resp.text
    objs = json.loads(resp.text)[0]['card_group']
    for obj in objs:
        print obj
    # html = BeautifulSoup(resp.text, from_encoding='gb2312')

if __name__ == '__main__':
    # fetch_weibo()
    print str('\xce\xe2\xd3\xa6\xb8\xbb')