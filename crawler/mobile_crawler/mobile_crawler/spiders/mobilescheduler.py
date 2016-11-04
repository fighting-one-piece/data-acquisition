# -*- coding:utf-8 -*-

import os
import sys
import time
import platform

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def startSeleniumServer():
    parent_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(parent_dir)[0]
    print parent_dir
    current_operation_system = platform.system()
    if current_operation_system == 'Windows':
        jar_file_path = os.path.join(parent_dir, 'driver', 'selenium-server-standalone-2.40.0.jar')
    elif current_operation_system == 'Linux':
        jar_file_path = os.path.join(parent_dir, 'driver', 'selenium-server-standalone-2.40.0.jar')
    print jar_file_path
    start_selenium_server_command = '''java -jar ''' + jar_file_path
    os.system(start_selenium_server_command)

if __name__ == '__main__':
    parent_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(parent_dir)[0]
    print parent_dir

    command = '''cd ''' + parent_dir + ''' & \
        scrapy crawl mobile_spider -s CLOSESPIDER_TIMEOUT=1800 & \
        '''
    while True:
        os.system(command)
        time.sleep(1800)
    # (status, output) = commands.getstatusoutput('ls ' + parent_dir)
    # print status
    # print output
