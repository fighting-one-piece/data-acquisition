#-*- coding:utf-8 -*-
'''
@author: wulin

'''

import json
import requests
from bs4 import BeautifulSoup


# video_url = 'http://api.t.iqiyi.com/qx_api/comment/get_video_comments? \
#         aid=11432559&albumid=203316801&categoryid=2&cb=fnsucc&escape=true& \
#         is_video_page=true&need_reply=true&need_subject=true&need_total=1& \
#         page=2&page_size=10&page_size_reply=3&qitan_comment_type=1& \
#         qitancallback=fnsucc&qitanid=11432559&qypid=01010011010000000000& \
#         reply_sort=hot&sort=hot&t=0.19584483513608575&tvid=490249400'

# video_url = 'http://www.iqiyi.com/v_19rrlfuf9w.html'

def handleComment(comment):
    print comment['content']
    if comment.has_key('userInfo') :
        userInfo = comment['userInfo']
        print 'uid %s uname %s profileUrl %s' %(userInfo['uid'], userInfo['uname'], userInfo['profileUrl'])
    if comment.has_key('sourceInfo') : 
        sourceInfo = comment['sourceInfo']
        print 'source %s' %sourceInfo['text']
    if comment.has_key('counterList') :
        counterList = comment['counterList']
        #"forwards":0,"replies":88,"likes":1089,"downs":0,"reads":0,"praises":0,"shares":0
        print 'replies %s likes %s downs %s' %(counterList['replies'], counterList['likes'], counterList['downs'])
    #print comment['keywords']['video_url']
    if comment.has_key('starInfo') :
        starInfo = comment['starInfo']
        print starInfo
    if comment.has_key('replyList') :
        replyList = comment['replyList']
        print 'replyList %s' %replyList
        for reply in replyList :
            handleComment(reply)

day_top_50_url = 'http://top.iqiyi.com/index/top50.htm?cid=2&dim=day'

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
    
    videoResponse = requests.get(comment_url)
    videoResponseText = videoResponse.text
    print videoResponseText
    #print json.loads(videoResponseText)['data']['comments'][1]['content']
    #print json.loads(videoResponseText)['data']['comments'][1]['contentId']
    comments = json.loads(videoResponseText)['data']['comments']
    i = 0
    for comment in comments :
        if i == 1 :
            break
        i = i + 1
        handleComment(comment)
