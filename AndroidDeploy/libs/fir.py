#-*- coding: utf-8 -*-
__author__ = 'geekwolf'

import  os
import  qrcode
import base64

class FirUtils():

    def __init__(self):

        self.token = 'Fir Token'
        self.message_url ='http://fir.im/simlinux?utm_source=fir&utm_medium=qr'

    def upload_apk(self):

        workspace = os.getenv('WORKSPACE')+"/app/build/outputs/apk/"
        version = os.popen("ls "+workspace+"|grep -vE  *unaligned|head -1|awk -F '-|.apk' \'{print $3}\' ").read().strip()

        if version:

            try:
                os.popen('fir login ' + self.token)
                fir_status = os.popen('fir publish ' + workspace + "app-debug-" + version + '.apk').read()
	    	print 'Fir 上传成功...'+'http://fir.im/simlinux' + '\t'+version	

                return  version
            except:
                sys.exit("Fir 上传失败!!!")
	

    def get_qrcode(self):

        img = qrcode.make(self.message_url)

        try:

            img.save('/tmp/simlinuxAqrcode.png')
            __pic = '/tmp/simlinuxAqrcode.png'
            f = open(__pic,'rb')
            pic_url = 'data:image/png;base64,' + base64.b64encode(f.read())
            f.close()
	    print "Qrcode二维码生成成功..." + '\t二维码访问地址:http://fir.im/simlinux'
        except:
            print 'Qrcode generation failure!!!'
        return pic_url,self.message_url
