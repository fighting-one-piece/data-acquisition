# -*- coding: utf-8 -*-

import sys
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

ACCOUNT = 'wulinshishen@sina.com'
PASSWORD = '@wulin1988'
SMTP_SERVER = 'smtp.163.com'

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def format_address(text):
    name, address = parseaddr(text)
    return formataddr((Header(name, 'utf-8').encode(), \
        address.encode('utf-8') if isinstance(address, unicode) else address))

def send_email(text):
    send_email('125906088@qq.com', text)

def send_email(to_address, text):
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = format_address(u'Mobile爬虫 <%s>' %ACCOUNT)
    message['To'] = format_address(u'DK <%s>' % to_address)
    message['Subject'] = Header(u'Mobile爬虫异常', 'utf-8').encode()

    server = smtplib.SMTP(SMTP_SERVER, 25)
    server.set_debuglevel(1)
    server.login(ACCOUNT, PASSWORD)
    server.sendmail(ACCOUNT, [to_address], message.as_string())
    server.quit()
