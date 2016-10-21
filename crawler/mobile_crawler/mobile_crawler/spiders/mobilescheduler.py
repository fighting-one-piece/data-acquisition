# -*- coding:utf-8 -*-

import os
import sys
import commands

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)


if __name__ == '__main__':
    parent_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(parent_dir)[0]
    print parent_dir
    command = '''cd ''' + parent_dir + ''' & \
        scrapy crawl mobile_spider -s CLOSESPIDER_TIMEOUT=1200 & \
        '''
    while True:
        os.system(command)
    # (status, output) = commands.getstatusoutput('ls ' + parent_dir)
    # print status
    # print output
