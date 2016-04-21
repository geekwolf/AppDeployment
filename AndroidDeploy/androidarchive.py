#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import os
import sys
import shutil
from libs.libsoss import OssUtils
from libs.dingtalk import DingTalkNotice
import hashlib
from oss.oss_api import *


class AndroidDeploy():

    def __init__(self):

        self.channel_to_deploy = str(os.getenv("ChannelToDeploy"))
        self.workspace = '/usr/share/tomcat/.jenkins/workspace/Android-Test'
        self.build_dir = self.workspace + '/app/build/outputs/apk/'
        self.channel_to_deploy = os.getenv('ChannelToDeploy')
        self.archive_pack_apk = '/data/android_archive/android/'
        #self.storepass = ''
        #self.keypass = ''
        #self.keystore = self.workspace+'/key.jks'

        if not os.listdir(self.build_dir):
		sys.exit('APK文件不存在,请先构建!!!')

        self.version = os.popen("ls "+ self.build_dir +"|grep -vE *unaligned|head -1|awk -F '-|.apk' '{print $3}'").read().strip()
	print self.version
        
        if self.version:
                self.now_apk =  self.build_dir + "app-release-"+ self.version + ".apk ".strip()
        else:
                sys.exit('APK文件不存在,请先构建2!!!')

        if not os.path.exists(self.archive_pack_apk + self.version):
            os.mkdir(self.archive_pack_apk + self.version)

        if not os.path.exists(self.build_dir + 'META-INF'):
            os.mkdir(self.build_dir + 'META-INF')

        self.archive_pack_apk_dir = self.archive_pack_apk + self.version + "/"



    def  archive_apk(self):
	
	 tag = os.popen('cd '+self.workspace+'&& git pull > /dev/null && git tag -l|grep  "^v[0-9]" |grep '+self.version).read().strip()

	 if tag:

	    print "已经创建发布时Tag:" + tag

	 else:
	   
	    try:
	        os.popen('cd '+self.workspace+' && git checkout master && git tag  V' + self.version + ' && git push  origin --tags ' + "V" + self.version)
	    except:
	     	sys.exit('Tag创建失败,请重新执行脚本!!!')

         if self.channel_to_deploy == 'All Channels':

            shutil.rmtree(self.archive_pack_apk + self.version)
            os.mkdir(self.archive_pack_apk + self.version)

            f = open(self.workspace + "/" + 'channels','r')
            for channel in f.readlines():

                channel = channel.strip()

                if channel == 'ma':
                     apk_name = 'MA'
               
                elif "_" in channel:
                     apk_name = 'ma_android'+ channel

                else:
                     apk_name = 'ma_android'+ "_" + channel
                try:
                   self.pack_apk(channel,self.archive_pack_apk_dir,apk_name)

                except:
                   sys.exit('签名失败,请检查!!!')
         else:

             if "_" in self.channel_to_deploy:
                apk_name = 'ma_android'+ self.channel_to_deploy
             else:
                apk_name = 'ma_android'+ "_" + self.channel_to_deploy
             self.pack_apk(self.channel_to_deploy,self.archive_pack_apk_dir,apk_name)
         
         return self.archive_pack_apk

    def pack_apk(self,channel,archive_pack_apk_dir,apk_name):
		
		old_channel_file = os.popen("unzip -l " + self.now_apk + "|grep 'META-INF/channel'|awk '{ print $NF }'").read().strip()
		print old_channel_file
		remove_old_channel_file = os.popen("cd " + self.build_dir + "&& zip -d " + self.now_apk + '\t' + old_channel_file).read().strip()
		new_channel_file = os.popen("cd " + self.build_dir + "&&touch " + "META-INF/channel_" + channel).read().strip()
		print new_channel_file
		os.popen( "cd " + self.build_dir + "&& zip -u " + self.now_apk + " " + "META-INF/channel_" + channel)
		print self.now_apk,archive_pack_apk_dir + apk_name.strip() + '.apk'
		dest = archive_pack_apk_dir + apk_name.strip() + '.apk'
		shutil.copyfile(self.now_apk,dest )
		
if __name__ == "__main__":

    pack = AndroidDeploy()
    libsoss = OssUtils()
    pack.archive_apk()
    version_dir = pack.version
    filespath = pack.archive_pack_apk + version_dir + "/"
    channel = pack.channel_to_deploy
    archive_download_url = libsoss.upload_oss(filespath,version_dir,channel)
    content = '各渠道正式包' + version_dir + '版本已经归档OSS(未发布),代码库已经自动创建发布Tag:' + version_dir + '访问地址为:http://download.simlinux.com/app/archive/' + version_dir +'/index.html'
    notice = DingTalkNotice()
    notice.post_msg(content=content)
