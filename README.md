####Android多渠道打包流程:
- 执行gradlew clean清除build目录
- 执行gradlew assemble编译打包Debug/Release(已自动签名)
- 上传Debug包到Fir
- 通过DingTalk发送通知信息到QA讨论组(发送提测apk包版本，下载地址及扫描下载二维码)
- 提测不通过，修复bug后再次执行前四步
- 提测通过后，点击Jenkins打包归档多渠道按钮，将执行生成多渠道包并归档包到本地目录/data/2.0.1/xxx.apk
- 可选择此步上传归档文件到OSS
- 点击Jenkins发布按钮将最新版本相关渠道归档拷贝至OSS发布目录
- 刷新CDN生效
- 通过DingTalk发送通知信息到QA讨论组哪些渠道已经发布

####IOS打包流程:
- xcodebuild clean 清理build目录
- xcodebuild archive 选择不同的环境/BundleID/ProvisionProfile/CodeSigningIdentify 编译，签名生成xcarchive文件
- xcodebuild -exportArchive 打包生成ipa
- 测试包自动上传Fir,生产包手动更新AppStore
####Android7.0打包方式:
- http://tech.meituan.com/android-apk-v2-signature-scheme.html
