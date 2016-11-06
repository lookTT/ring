#!/bin/bash

#判断参数个数是否正确
if [[ $# != 1 ]]; then
    echo "bad aparameterrg num: expect 1 get $#"
    exit
fi

#获取参数
domain=$1
echo "start searching: "$domain

#生成uuid
uuid=`uuid`
#生成时间
curDate=`date +%Y-%m-%d_%H_%M_%S`
#创建文件夹
dirpath='/tmp/'$domain'__'$curDate'___'$uuid'/'
mkdir $dirpath

#开始执行域名及IP搜索
echo "start to execute wydomain script"
cd wydomain
# 执行穷举
python dnsburte.py -d $domain -f default.csv -o $domain'.dnsburte.log'
# 执行API查询目标的子域名
python wydomain.py -d $domain -o $domain'.wydomain.log'
# 执行baidu查询目标的字域名
luajit baiduSubDomain.lua $domain

echo "Search SubDomain complate, The result has been saved in ./result/$domain"

echo "start wydomainSave2DB.py"
#将文件内的域名信息保存

cd ../wycommon
filefullpath="../wydomain/result/"$domain"/"
python wydomainSave2DB.py $uuid $domain $filefullpath

# #跑nmap相关
# echo "start to execute wyportmap script"
# #生成文件的绝对路径以及文件名
# filename='wyportmap.txt'
# filefullpath=$dirpath$filename
# echo "wyportmap.txt fullpath:"$filefullpath
# #将mysql中的数据写入文件
# echo "start wyportmapTransfer.py"
# cd ../wycommon
# python wyportmapTransfer.py $uuid $filefullpath

# #进入wyportmap目录
# echo "start wyportmap.py"
# cd ../wyportmap/
# #读取临时文件 执行脚本
# cat $filefullpath | while read myline
# do 
#     echo "read IP:["$myline"]to Execute the script"
#     nohup python wyportmap.py $myline $uuid > $dirpath"_wyportmap__"$myline".txt"  2>&1 &
# done

echo "start to execute weakfilescan/wyspider.py script"
cd ../weakfilescan
#敏感信息泄露检测工具
#生成文件的绝对路径以及文件名
filename='weakfilescan.txt'
filefullpath=$dirpath$filename
echo "weakfilescan.txt fullpath:"$filefullpath
python wyspider.py $domain $filefullpath

echo "start to execute wycommon/wyweakfilescanSave2DB.py script"
cd ../wycommon
python wyweakfilescanSave2DB.py $uuid $filefullpath

echo "Done"
