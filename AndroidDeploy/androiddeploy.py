#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import os
import sys
import shutil
from libs.libsoss import OssUtils
from libs.dingtalk import DingTalkNotice
from libs.chinanetcenter import ChinaNetCenter
import hashlib
from oss.oss_api import *


if __name__ == "__main__":

    libsoss = OssUtils()
    url_list = libsoss.copy_oss()
    content = '_11到_40,渠道包已经上线,可通过http://download.simlinux.com/app/ma_android_11.apk访问,相关CDN地址已经刷新!!!'
    chinanetcenter = ChinaNetCenter()
    chinanetcenter.flush_files(url_list)
    notice = DingTalkNotice()
    notice.post_msg(content=content)
