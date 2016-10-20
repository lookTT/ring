#!/bin/bash

#判断参数个数是否正确
if [[ $# != 1 ]]; then
    echo "bad aparameterrg num: expect 1 get $#"
    exit
fi

#生成uuid
uuid=`uuid`
#生成时间
curDate=`date +%Y-%m-%d_%H_%M_%S`
#创建文件夹
dirpath='/tmp/'$curDate'___'$uuid'/'
mkdir $dirpath
#生成文件的绝对路径以及文件名
filename='wydomain.txt'
filefullpath=$dirpath$filename

#开始执行域名及IP搜索
echo "start to execute wydomain script"
cd wydomain
python wydomain.py $1 $filefullpath

#将文件内的域名信息保存
cd ../wycommon
python wydomainSave2DB.py $uuid $1 $filefullpath

#跑nmap相关
echo "start to execute wyportmap script"
#生成文件的绝对路径以及文件名
filename='wyportmap.txt'
filefullpath=$dirpath$filename
#将mysql中的数据写入文件
cd ../wycommon
python wyportmapTransfer.py $uuid $filefullpath
#进入wyportmap目录
cd ../wyportmap/
#读取临时文件 执行脚本
cat $filefullpath | while read myline
do 
    echo "read IP:["$myline"]to Execute the script"
    nohup python wyportmap.py $myline $uuid > $dirpath"_wyportmap__"$myline".txt"  2>&1 &
done

cd ../weakfilescan
#敏感信息泄露检测工具
#生成文件的绝对路径以及文件名
filename='weakfilescan.txt'
filefullpath=$dirpath$filename
python wyspider.py $1

echo "Done"
