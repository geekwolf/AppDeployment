#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import os
import re
import sys
import hashlib
from oss.oss_api import *
from itertools import islice
import  oss2

class OssUtils():

    def __init__(self):

        self.workspace = '/usr/share/tomcat/.jenkins/workspace/Android-Test'
        self.endpoint="oss-cn-beijing.aliyuncs.com"
        self.accessKeyId, self.accessKeySecret="",""
        self.oss = OssAPI(self.endpoint, self.accessKeyId, self.accessKeySecret)
        self.header={"Cache-Control":"max-age=31536000","Content-Type":"application/vnd.android.package-archive"}
        self.bucket='staticfiles'
        self.filespath=''

    def upload_oss(self,filespath,version_dir,channel):
        
        version_dir = version_dir + "/"
        if channel == 'All Channels':

            listfile=os.listdir(filespath)
            file = '/tmp/index.html'
            os.remove(file)
            f=open('/tmp/index.html','a')
            
            for src in listfile:

                __channel_tmp = re.split('_|.apk',src)

                try:

                    res=self.oss.put_object_from_file(self.bucket,"app/archive/"+ version_dir +src,filespath+src,headers=self.header)

                    if __channel_tmp[0] == 'MA':
                        __channel = 'MA'
                    else:
                        __channel = __channel_tmp[2]

                        f.write('<b>'+ __channel + '</b>' +'\t<a href=/app/archive/' + version_dir + str(src) + '>' + 'http://download.simlinux.com/app/archive/'+ version_dir + str(src) + '</a><br>')
                except:
                    
                    system.exit('上传不完整或失败!!!')
            
            res=self.oss.put_object_from_file(self.bucket,"app/archive/"+ version_dir + 'index.html',file,headers={"Content-Type":"text/html"})

            f.close()

        else:
            try:
                src = os.popen('cd '+ filespath +';ls *' + channel + '* ').read().strip()
                res = self.oss.put_object_from_file(self.bucket,"app/archive/"+ version_dir + src,filespath + src,headers=self.header)
            except:

                system.exit('上传不完整或失败!!!')

        archive_download_url = 'http://download.simlinux.com/app/archive/' + version_dir + 'index.html'
        return archive_download_url

    def copy_oss(self):

        auth = oss2.Auth(self.accessKeyId,self.accessKeySecret)
        bucket = oss2.Bucket(auth,self.endpoint,self.bucket)
	latest_version = max(os.popen('cd '+self.workspace+'&& git pull > /dev/null && git tag -l|grep  "^v[0-9]"').read().strip().split("\n")).replace('v','')
        apk_name = 'app/archive/' + latest_version + '/' + 'MA.apk'
        dest_name = 'app/' + latest_version + '/' + 'MA.apk'
        result = bucket.copy_object(self.bucket, apk_name , dest_name)	
	url_list = []

        #要发布渠道11-41,可根据自身情况改写
        for channel in range(11,41):
	
            apk_name = 'app/archive/' + latest_version + '/ma_android_'+ str(channel) + '.apk'
            dest_name = 'app/' + latest_version + '/' + 'ma_android_'+ str(channel) + '.apk'
	    url_list.append('http://download.simlinux.com/app/' + 'ma_android_'+ str(channel) + '.apk')
            result = bucket.copy_object(self.bucket, apk_name , dest_name)
            if result.resp.status == 200:
                print 'APK发布:由' + apk_name + '\t----->\t' + dest_name
            else:
                sys.exit('APK拷贝失败,请重试!!!')
	url_list.append('http://download.simlinux.com/app/' + 'MA.apk')		
        return url_list
