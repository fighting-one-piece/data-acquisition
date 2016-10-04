# -*- coding:utf-8 -*-

import sys
from selenium import webdriver

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def csdn_login(username, password):
    driver = webdriver.PhantomJS(executable_path='F:\\develop\\crawler\\phantomjs-2.1.1\\bin\\phantomjs.exe')
    driver.get('http://passport.csdn.net/account/login')
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_class_name('logging').click()
    for item in driver.get_cookies():
        print item

def iteye_login(username, password):
    driver = webdriver.PhantomJS(executable_path='F:\\develop\\crawler\\phantomjs-2.1.1\\bin\\phantomjs.exe')
    driver.get('http://www.iteye.com/login')
    driver.find_element_by_id('user_name').clear()
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('user_name').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('button').click()
    for item in driver.get_cookies():
        print item

def qqqun_login(username, password):
    driver = webdriver.PhantomJS(executable_path='F:\\develop\\crawler\\phantomjs-2.1.1\\bin\\phantomjs.exe')
    driver.get('http://qqun.qq.com/group/login.html')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('u').send_keys(username)
    driver.find_element_by_id('p').send_keys(password)
    driver.find_element_by_id('login_button').click()
    for item in driver.get_cookies():
        print item

if __name__ == '__main__':
    # iteye_login('wulinshishen', '5201314')
    qqqun_login('478953009', '@laji5201314')
