#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import requests
import  json
import datetime
import  hashlib

class ChinaNetCenter():

    def __init__(self):

        self.username = '推送用户'
        self.password = '推送密码'

    def flush_files(self,url_list):
	#print url_list
        time = datetime.datetime.now().strftime("%Y%m%d")
        headers = {'content-type': 'application/json'}
        post_url = 'http://cm.chinanetcenter.com/CM/cm-publish!json.do'
        check_code = hashlib.new("md5", time + self.username + 'chinanetcenter' + self.password).hexdigest()
	    __content = {"user_name":self.username,"check_code":check_code,"need_feedback":"0","fetchOption":"N","url_list":url_list}
        content = json.dumps(__content)
	    print content
        try:
            r = requests.post(post_url, data=content, headers=headers)
	    print r.text
        except:
            print '刷新失败,请重试!!!'

