#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
import uuid
import random
import hashlib
import urllib2
import traceback
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class crypt(object):
    __iv = '0102030405060708'
    __mode = AES.MODE_CBC
    __BS = AES.block_size
    is_changing = False

    # uid = '88800008552822'
    # tk = '893aeb7c5cd24e33b121ad82dfeff3fb'
    # sk = 'd4GHttr7dYH9iSjj'

    uid = '88800008574135'
    tk = 'b560225fdbef44e6b7e1a9c191b819c7'
    sk = '0uUrWMbjLefmuBcr'

    @staticmethod
    def encrypt_register(text):
        __pad = lambda s: s + (crypt.__BS - len(s) % crypt.__BS) * chr(crypt.__BS - len(s) % crypt.__BS)
        text = __pad(text)
        crypt.obj1 = AES.new('ws@7JJzpj$g#s1Db', crypt.__mode, crypt.__iv)
        crypt.ciphertext = crypt.obj1.encrypt(text)
        return b2a_hex(crypt.ciphertext)

    @staticmethod
    def decrypt_register(text):
        __unpad = lambda s: s[0:-ord(s[-1])]
        crypt.obj2 = AES.new('ws@7JJzpj$g#s1Db', crypt.__mode, crypt.__iv)
        plain_text = crypt.obj2.decrypt(a2b_hex(text))
        return __unpad(plain_text.rstrip('\0'))

    @staticmethod
    def encrypt_mobile(text):
        __pad = lambda s: s + (crypt.__BS - len(s) % crypt.__BS) * chr(crypt.__BS - len(s) % crypt.__BS)
        text = __pad(text)
        crypt.obj1 = AES.new(crypt.sk, crypt.__mode, crypt.__iv)
        crypt.ciphertext = crypt.obj1.encrypt(text)
        return b2a_hex(crypt.ciphertext)

    @staticmethod
    def decrypt_mobile(text):
        __unpad = lambda s: s[0:-ord(s[-1])]
        crypt.obj2 = AES.new(crypt.sk, crypt.__mode, crypt.__iv)
        plain_text = crypt.obj2.decrypt(a2b_hex(text))
        return __unpad(plain_text.rstrip('\0'))

    @staticmethod
    def encrypt_mobile_sk(text, sk):
        __pad = lambda s: s + (crypt.__BS - len(s) % crypt.__BS) * chr(crypt.__BS - len(s) % crypt.__BS)
        text = __pad(text)
        crypt.obj1 = AES.new(sk, crypt.__mode, crypt.__iv)
        crypt.ciphertext = crypt.obj1.encrypt(text)
        return b2a_hex(crypt.ciphertext)

    @staticmethod
    def decrypt_mobile_sk(text, sk):
        __unpad = lambda s: s[0:-ord(s[-1])]
        crypt.obj2 = AES.new(sk, crypt.__mode, crypt.__iv)
        plain_text = crypt.obj2.decrypt(a2b_hex(text))
        return __unpad(plain_text.rstrip('\0'))

    @staticmethod
    def change_auth():
        try:
            crypt.is_changing = True
            url = 'http://address.imcaller.com/wp/woa/v1/device.json'
            imei = random.randint(100000000000000, 999999999999999)
            did = str(uuid.uuid1()).replace('-', '')[0:16]
            data = '{"pfm":"android","imei":"' + str(imei) + '","pid":"8888888","did":"' + did + '","vcode":81}'
            postStr = "{\"data\":\"" + crypt.encrypt_register(data) + "\"}"
            req_header = {
                'X-CLIENT-PFM': '20',
                'X-CLIENT-VCODE': '81',
                'X-CLIENT-PID': '8888888',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 2 MIUI/V7.5.5.0.LHMCNDE',
                'Accept-Encoding': 'gzip',
            }
            req_timeout = 50
            req = urllib2.Request(url=url, headers=req_header, data=postStr)
            resp = urllib2.urlopen(req, None, req_timeout)
            html = resp.read()
            jsonobj = json.loads(html)
            if str(jsonobj['resultCode']) != '0':
                return False
            else:
                jsonobj = json.loads(crypt.decrypt_register(json.loads(html)["data"]))
                crypt.uid = jsonobj['uid']
                crypt.sk = jsonobj['sk']
                crypt.tk = jsonobj['tk']
                return True
        except Exception, e:
            print e.message
            print traceback.format_exc()
            return False
        finally:
            crypt.is_changing = False

    @staticmethod
    def get_posturl():
        return "http://address.imcaller.com/wp/harass/v1/query_call.json?tk=" + crypt.tk \
               + "&crc=" + crypt.encrypt_mobile(crypt.uid + "_" + str(time.time()))

    @staticmethod
    def get_poststr(mobile):
        data = "{\"uid\":\"" + crypt.uid + "\",\"p\":\"" + mobile + "\",\"type\":\"stranger\",\"trigger\":\"normal\"}"
        postStr = "{\"data\":\"" + crypt.encrypt_mobile(data) + "\"}"
        return postStr

    @staticmethod
    def get_md5(text):
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()