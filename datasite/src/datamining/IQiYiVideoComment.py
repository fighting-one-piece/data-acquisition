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
        if replyList is not None :
            for reply in replyList :
                handleComment(reply)

url_dianshiju = 'http://top.iqiyi.com/index/top50.htm?cid=2&dim=day'
url_dianying = 'http://top.iqiyi.com/dianying.html#vfrm=7-13-0-1'
url_zongyi = 'http://top.iqiyi.com/zongyi.html#vfrm=7-13-0-1'
url_yule = 'http://top.iqiyi.com/yule.html#vfrm=7-13-0-1'
url_dongman = 'http://top.iqiyi.com/dongman.html#vfrm=7-13-0-1'
url_zixun = 'http://top.iqiyi.com/zixun.html#vfrm=7-13-0-1'
url_yuanchuang = 'http://top.iqiyi.com/yuanchuang.html#vfrm=7-13-0-1'
url_pianhua = 'http://top.iqiyi.com/pianhua.html'
url_shaoer = 'http://top.iqiyi.com/shaoer.html#vfrm=7-13-0-1'
url_yinyue = 'http://top.iqiyi.com/yinyue.html#vfrm=7-13-0-1'
url_jiaoyu = 'http://top.iqiyi.com/jiaoyu.html#vfrm=7-13-0-1'
url_weidianying = 'http://top.iqiyi.com/weidianying.html#vfrm=7-13-0-1'
url_caijing = 'http://top.iqiyi.com/caijing.html#vfrm=7-13-0-1'
url_guanggao = 'http://top.iqiyi.com/guanggao.html#vfrm=7-13-0-1'
url_qiche = 'http://top.iqiyi.com/qiche.html#vfrm=7-13-0-1'
url_youxi = 'http://top.iqiyi.com/youxi.html#vfrm=7-13-0-1'
url_gaoxiao = 'http://top.iqiyi.com/gaoxiao.html#vfrm=7-13-0-1'
url_shenghuo = 'http://top.iqiyi.com/shenghuo.html#vfrm=7-13-0-1'
url_tiyu = 'http://top.iqiyi.com/tiyu.html#vfrm=7-13-0-1'
url_jilupian = 'http://top.iqiyi.com/jilupian.html#vfrm=7-13-0-1'
url_shishang = 'http://top.iqiyi.com/shishang.html#vfrm=7-13-0-1'
url_lvyou = 'http://top.iqiyi.com/lvyou.html#vfrm=7-13-0-1'
url_junshi = 'http://top.iqiyi.com/junshi.html#vfrm=7-13-0-1'
url_paike = 'http://top.iqiyi.com/paike.html#vfrm=7-13-0-1'
url_muying = 'http://top.iqiyi.com/muying.html#vfrm=7-13-0-1'
url_keji = 'http://top.iqiyi.com/keji.html#vfrm=7-13-0-1'
url_talkshow = 'http://top.iqiyi.com/talkshow.html#vfrm=7-13-0-1'
url_health = 'http://top.iqiyi.com/health.html#vfrm=7-13-0-1'

day_top_50_url_list = [url_dianshiju, url_dianying, url_zongyi, url_yule, url_dongman, 
        url_zixun, url_yuanchuang, url_pianhua, url_shaoer, url_yinyue, url_jiaoyu, 
        url_weidianying, url_caijing, url_guanggao, url_qiche, url_youxi, url_gaoxiao, 
        url_shenghuo, url_tiyu, url_jilupian, url_shishang, url_lvyou, url_junshi, 
        url_paike, url_muying, url_keji, url_talkshow, url_health]


for day_top_50_url in day_top_50_url_list :
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
        if flashBoxDiv is None : continue
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
