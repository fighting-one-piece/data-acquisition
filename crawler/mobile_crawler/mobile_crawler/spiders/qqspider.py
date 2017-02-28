# -*- coding: utf-8 -*-

import sys
import random
import requests
from bs4 import BeautifulSoup

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def a():
    url = 'https://aq.qq.com/cn2/unionverify/pc/pc_uv_show?info=Sjwn3QpLMtu90fERcm4NLQS0feYm_bcrhH6JFZdGIaBandnsupIHtQIhcs0KQ7DpNApVfNAGVYkSi7EnbHJeAjiI4q9pL-hv1SMWVSLdFQxDcdUDfjjUyRiVEOokcELYDQRlN-SlzS6pG5eKgxAbnSLXDI5DPOK40h5fiQJUNrXo3L5ERmUzdN93Ivlz7UWyh--cckqdJtFM-IU5iXsnLjQ**&session_context=3'
    response = requests.get(url)
    print response.text
    html = BeautifulSoup(response.text, 'html.parser')
    print html.select('p.wording_1')[0].contents

def b():
    qq = '1106439835'
    url = 'https://aq.qq.com/cn2/uv_aq/pc/aj_mb_mobile?mobile_verify_type=2'
    req_session = requests.session()
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "https://aq.qq.com/v2/uv_aq/html/reset_pwd/pc_reset_pwd_uv_aq_verify.html?s=3",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
               "Cookie": "tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; ptui_loginuin=478953009; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0478953009; o_cookie=125906088; pgv_pvid=512697556; p_o2_uin=125906088; ptisp=ctc; aq_base_sid=loPYar3XTQbzEXfHTEKxPd4eywXCJxSZ; pgv_si=s3063432192; aq_log_src_id=0; sceneId=; jump_name=pc_find_pwd; IsMobileForb=0; sceneid=none; verifysession=h014a6fb2add461b922f3c494edff7efc505cc0cf0b0eb1c14f193fd5a8a6ef1fa1a8783fad6982ea06a99103dbc32afa3a"
               # "Cookie": "tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; ptui_loginuin=" + qq + "; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0478953009; o_cookie=125906088; pgv_pvid=512697556; p_o2_uin=125906088; ptisp=ctc; aq_base_sid=loPYar3XTQbzEXfHTEKxPd4eywXCJxSZ; pgv_si=s3063432192; aq_log_src_id=0; sceneId=; jump_name=pc_find_pwd; IsMobileForb=0; sceneid=none; verifysession=h014a6fb2add461b922f3c494edff7efc505cc0cf0b0eb1c14f193fd5a8a6ef1fa1a8783fad6982ea06a99103dbc32afa3a"
               # "Cookie": "tvfe_boss_uuid=79f00b58115ca0a7; AMCV_248F210755B762187F000101%40AdobeOrg=793872103%7CMCIDTS%7C16953%7CMCMID%7C66043914376763604261923396171884197480%7CMCAAMLH-1465275557%7C11%7CMCAAMB-1465275557%7CNRX38WO0n5BH8Th-nqAG_A%7CMCAID%7CNONE; pac_uid=1_125906088; pgv_pvi=9364808704; RK=DRHXD9GnNs; ptui_loginuin=1106439835; ptcz=9144862ee33d9a30089d6135cd94fdda6a64126f1fcd49ecc8d5df3289410284; pt2gguin=o0478953009; o_cookie=125906088; pgv_pvid=512697556; p_o2_uin=125906088; ptisp=ctc; aq_base_sid=loPYar3XTQbzEXfHTEKxPd4eywXCJxSZ; pgv_si=s3063432192; aq_log_src_id=0; sceneId=; jump_name=pc_find_pwd; IsMobileForb=0; sceneid=none; verifysession=h014a6fb2add461b922f3c494edff7efc505cc0cf0b0eb1c14f193fd5a8a6ef1fa1a8783fad6982ea06a99103dbc32afa3a"
               }
    response = req_session.get(url, headers=headers)

    print response.text

def c():
    url = 'http://cq.hanfenghupan.com/Vote/SubmitVote?_=1478489477071'
    data = {'sid': '0E72EB81-1FA2-40B7-B17D-4DB0B0C606AD', 'iid': 'FAA6825C-7A11-47DE-80D0-549B13EC6399'}
    # cookie = 'ASP.NET_SessionId=xxiaztshvacpscmz4xxqs2dk'
    # response = requests.post(url, data=data)

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'cq.hanfenghupan.com',
        # 'Cookie': 'ASP.NET_SessionId=xxiaztshvacpscmz4xxqs2dk',
        # 'Cookie': 'ASP.NET_SessionId=bfutakj2ti5bbldulkgiqf0c',
        # 'Cookie': 'ASP.NET_SessionId=gcpbbcximx4rjqylkggsma5i',
        'Cookie': 'ASP.NET_SessionId=nfna1q4qonishowwt1y1s34q',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        # 'Referer': 'http://cq.hanfenghupan.com/vote/index?sid=0E72EB81-1FA2-40B7-B17D-4DB0B0C606AD&code=021ifoCc1i9Z7t0ky2Bc1zxjCc1ifoCT&state=STATE'
        'Referer': 'http://cq.hanfenghupan.com/vote/index?sid=0E72EB81-1FA2-40B7-B17D-4DB0B0C606AD&code=012ifoCc1i9Z7t0ky2Bc1zxjCc1ifoCT&state=STATE'
        }
    response = requests.post(url, data=data, verify=False, headers=headers)
    print response.text

def weibo_authorize_code():
    url = 'https://api.weibo.com/oauth2/authorize?client_id=1364975478&response_type=code&redirect_uri=https://api.weibo.com/oauth2/default.html'
    response = requests.get('url')
    print response.content

def weibo_access_token():
    url = 'https://api.weibo.com/oauth2/access_token'
    data = {'client_id': '1364975478', 'client_secret': '1e4f2a5e7b1040d8fbf86db76a349e2a', 'grant_type': 'authorization_code',
            'code': '0aa0b9c9f14433df63914448b4108a39', 'redirect_uri':'https://api.weibo.com/oauth2/default.html'}
    response = requests.post(url, data=data, verify=False)
    print response.text
    # '00saxW1EWTS4UB0ec44b04c806dI2o'

def weibo_followers():
    url = 'https://api.weibo.com/2/friendships/followers.json'
    params = {'access_token': '00saxW1EWTS4UB0ec44b04c806dI2o', 'uid': '3967913626', 'count': 20}
    response = requests.get(url, params=params, verify=False)
    print response.text

def weibo_following_user():
    url = 'https://api.weibo.com/2/friendships/create.json'
    data = {'access_token': '00saxW1EWTS4UB0ec44b04c806dI2o', 'uid': '3967913626'}
    response = requests.post(url, data=data, verify=False)
    print response.text


if __name__ == '__main__':
    for i in xrange(20):
        print i
        random_num = random.randint(1, 9)
        print 'random: %s %s' %(random_num, random_num * 1111)
    str1 = '1,1'
    print str1.find(':')
    print str1.split(',')
    content = '_b'
    if content.startswith('_'):
        print content[1:]