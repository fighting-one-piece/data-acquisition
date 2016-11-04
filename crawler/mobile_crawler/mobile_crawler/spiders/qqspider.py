# -*- coding: utf-8 -*-

import sys
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
    url = ''

if __name__ == '__main__':
    b()