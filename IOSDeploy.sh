#!/bin/sh

#说明依赖xcode工具集和fir(ruby包),by 公司ioser-lijing
export LC_ALL=zh_CN.UTF-8;export LANG=zh_CN.UTF-8

now=$(date +"%Y_%m_%d-%H_%M")

projectname="IOS_TEST_DEMO"
path_project="~/Desktop/workspace/${projectname}/"
path_output_root="~/Desktop/buildtool/"
path_workspace="$path_project/$p{rojectname}.xcworkspace"

#info
buildConfig=""
scheme=""
infoPlist=""
version_project=""
buildversion_project=""
bundleid_project=""
provisioning_profile=""
code_sign_identity=""
export_option_plist=""
path_export=""

if [[ ! -d $path_project ]];then
    echo "项目目录错误:\n$path_project"
    exit
fi

if [[ ! -d $path_output_root ]];then
    mkdir -p $path_output_root
fi

function project_info(){
    local plist=$1
    version_project=`/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" $plist`
    buildversion_project=`/usr/libexec/PlistBuddy -c "Print CFBundleVersion" $plist`
}

# function set_bversion(){
#     local plist=$1
#     lastversion=project_build_version
#     echo "$lastversion"
#     newversion=100
#     `/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $newversion" "$plist"`
# }

#询问打包环境
trap "echo -e \"\n已中断执行\";exit 0" INT
for((i=1;i<=100;i++));do
        read -n1 -p "打包是否为国内版[y/n]:" input
        if [ "$input" == "y" ] ; then
        	is_chin=true
        	break
        else
        	if [ "$input" == "n" ]; then
        		is_chin=false
        		break
        	else
        		echo "输入有误"
        	fi
        fi      
        input=""   
done

echo ""

for((i=1;i<=100;i++));do
        read -n1 -p "打包是否为测试版[y/n]:" input
        if [ "$input" == "y" ] ; then
        	is_fir=true
        	break
        else
        	if [ "$input" == "n" ]; then
        		is_fir=false
        		break
        	else
        		echo "输入有误"
        	fi
        fi      
        input=""   
done

echo ""

#整理打包所需材料
if $is_chin ; then
	#statements
	scheme="Demo_CN"
	infoPlist="${path_project}${projectname}/${scheme}_Info.plist"
    echo "$infoPlist"
    project_info $infoPlist
	if $is_fir ; then
		#statements
        buildConfig="Debug"

        bundleid_project="com.simlinux.demo"
        provisioning_profile="dc2117ff-9bfe-4234-8047-01d220238fdb"
        code_sign_identity="Demo Communication Co., Ltd"
		
        name_output="${scheme}-FIR_v${version_project}(b${buildversion_project})_${now}"
        export_option_plist="${path_output_root}/plist/FirExportOptions.plist"
         echo "国内测试包"
	else
        buildConfig="Release"

        bundleid_project="com.simlinux.demo"
        provisioning_profile="dc2117ff-9bfe-4234-8047-01d220238fdb"
        code_sign_identity="Demo Communication Co., Ltd"
		
        name_output="${scheme}-APS_v${version_project}(b${buildversion_project})_${now}"
        export_option_plist="${path_output_root}/plist/AppstoreExportOptions.plist"
        echo "国内正式包"
	fi
	
else
	scheme="Demo_Inter"
	infoPlist="${path_project}${projectname}/${scheme}_Info.plist"
    project_info $infoPlist
	if $is_fir ; then
		#statements
        buildConfig="Debug"

        bundleid_project="com.simlinux.demo"
        provisioning_profile="dc2117ff-9bfe-4234-8047-01d220238fdb"
        code_sign_identity="Demo Communication Co., Ltd"
		
        name_output="${scheme}-FIR_v${version_project}(b${buildversion_project})_${now}"
        export_option_plist="${path_output_root}/plist/FirExportOptions.plist"
        echo "国际测试包"
	else
        buildConfig="Release"

        bundleid_project="com.simlinux.demo"
        provisioning_profile="dc2117ff-9bfe-4234-8047-01d220238fdb"
        code_sign_identity="Demo Communication Co., Ltd"
		
        name_output="${scheme}-APS_v${version_project}(b${buildversion_project})_${now}"
        export_option_plist="${path_output_root}/plist/AppstoreExportOptions.plist"
        echo "国际正式包"
	fi
fi

path_export="${path_output_root}/${scheme}/${name_output}"
path_archive="${path_export}/$scheme.xcarchive"

#clean
xcodebuild clean -workspace ${path_workspace} -scheme ${scheme} -configuration ${buildConfig}

#archive
xcodebuild -workspace ${path_workspace} -scheme ${scheme} -configuration ${buildConfig} archive -archivePath ${path_archive} CODE_SIGN_IDENTITY="${code_sign_identity}" PROVISIONING_PROFILE="${provisioning_profile}" PRODUCT_BUNDLE_IDENTIFIER=${bundleid_project}

#ipa
xcodebuild -exportArchive -archivePath ${path_archive} -exportPath ${path_export} -exportOptionsPlist ${export_option_plist}

if $is_fir ; then
    #statements
    #上传到Fir
    api_token_fir="Fir Token"
    fir login $api_token_fir
    ipaPath="${path_export}/${scheme}.ipa"
    echo "$ipaPath"
    fir publish $ipaPath
fi


#上传到AppStore


