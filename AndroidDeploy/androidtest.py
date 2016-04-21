#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

from  libs.fir import FirUtils
from libs.dingtalk import DingTalkNotice
import requests
import requests.packages.urllib3.util.ssl_
print(requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


if __name__ == "__main__":

    fir = FirUtils()
    version = fir.upload_apk()
    pic_msg_url = fir.get_qrcode()
    title ='Android测试发布'
    text = '本次发布为Debug-' + version + ',已经上传fir,请扫描二维码安装!'
    notice = DingTalkNotice()
    notice.send_link(title=title,text=text,pic_url=pic_msg_url[0],message_url=pic_msg_url[1])
