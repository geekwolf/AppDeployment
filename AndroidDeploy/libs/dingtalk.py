#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import  json
import requests
import  os
import  qrcode
import base64
import requests.packages.urllib3.util.ssl_
print(requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

class DingTalkNotice():

    def __init__(self,**kwargs):

        #self.source_image = ''
        self.sender = "发送这ID"
        self.chat_id = '会话ID'

    def get_token(self):

        get_url = 'https://oapi.dingtalk.com/gettoken?corpid=钉钉后台coreid&corpsecret=钉钉后台coresecret'

        try:
            r = requests.get(get_url)
        except:
            print "DingTalk token获取失败!!!"

        data = json.loads(r.content)
        access_token = data['access_token']
        return access_token

    def post_images(self):
    
        __access_token = self.get_token()
        headers = {'content-type': 'application/json'}
        post_url = 'https://oapi.dingtalk.com/media/upload?access_token=' + __access_token + '&type=image'
        files = {'media': open(self.source_img,'rb')}
        try:
            r = requests.post(post_url, files=files)
            media_id = json.loads(r.text)['media_id']
            templates = {"chatid": self.chat_id,"sender":self.sender,"msgtype":"image","image":{"media_id":media_id}}
            post_data = json.dumps(templates)
            r = requests.post(post_url, data=post_data, headers=headers)
    
        except:
            print "DingTalk POST数据失败!!!"
    
        return r.text

    def post_msg(self,content):

        __access_token = self.get_token()

        headers = {'content-type': 'application/json'}
        post_url = 'https://oapi.dingtalk.com/chat/send?access_token=' + __access_token
        templates = { "chatid": self.chat_id, "sender": self.sender,"msgtype": "text", "text": { "content": content }}
        post_data = json.dumps(templates)
        try:
            r = requests.post(post_url, data=post_data, headers=headers)
            if  json.loads(r.content)['errmsg'] != 'ok':
                print "发送者ID不存在(sender)"
        except:
            print "DingTalk POST数据失败!!!"

        return r.text

    def send_link(self,title,text,pic_url,message_url):

        __access_token = self.get_token()

        headers = {'content-type': 'application/json'}
        post_url = 'https://oapi.dingtalk.com/chat/send?access_token=' + __access_token
        templates = {"chatid":self.chat_id ,"sender":self.sender,"msgtype":"link","link":{"title": title ,"text": text,"pic_url": pic_url,"message_url":message_url}}
        post_data = json.dumps(templates)
        try:
            r = requests.post(post_url, data=post_data, headers=headers)
            print r.text
        except:
            print "DingTalk POST数据失败!!!"
