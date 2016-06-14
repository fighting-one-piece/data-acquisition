# -*- coding:utf-8 -*-
'''
@author: wulin

'''

import requests

from bs4 import BeautifulSoup

#
day_top_50_url = 'http://top.iqiyi.com/index/top50.htm?cid=2&dim=day'

# 
movie_url = 'http://top.iqiyi.com/dianying.html#vfrm=7-13-0-1'

response = requests.get(day_top_50_url)
responseText = response.text
bs = BeautifulSoup(responseText, "html.parser")
lis = bs.select('ul.tv_list li a.toplay')
for li in lis:
    video_url = li['href']
    videoResponse = requests.get(video_url)
    videoResponseText = videoResponse.text
    videoBS = BeautifulSoup(videoResponseText, "html.parser")
    flashBoxDiv = videoBS.find(id="flashbox")
    albumid = flashBoxDiv.get('data-player-albumid')
    tvid = flashBoxDiv.get('data-player-tvid')
    
    qiTanCommonAreaDiv = videoBS.find(id="qitancommonarea")
    qitanid = qiTanCommonAreaDiv.get('data-qitancomment-qitanid')
    
    comment_url = 'http://api.t.iqiyi.com/qx_api/comment/get_video_comments? \
            aid=$aid$&albumid=$albumid$&categoryid=2&cb=fnsucc&escape=true& \
            is_video_page=true&need_reply=true&need_subject=true&need_total=1& \
            page=2&page_size=10&page_size_reply=3&qitan_comment_type=1& \
            qitancallback=fnsucc&qitanid=$qitanid$&qypid=01010011010000000000& \
            reply_sort=hot&sort=hot&tvid=$tvid$'
            
    comment_url = comment_url.replace('$aid$', qitanid)
    comment_url = comment_url.replace('$albumid$', albumid)
    comment_url = comment_url.replace('$qitanid$', qitanid)
    comment_url = comment_url.replace('$tvid$', tvid)
    
    print comment_url

        
        
