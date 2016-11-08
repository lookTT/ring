#!/bin/bash

echo "$$">>pid.txt

#获取参数
domain=
uuid=

#判断参数个数是否正确
if [[ $# -eq 1 ]]; then
    domain=$1
    uuid=`uuid`
elif [[ $# -eq 2 ]]; then
    domain=$1
    uuid=$2
else
    echo "bad aparameterrg num: expect 1 get $#"
    exit
fi

# #生成uuid
# uuid=`uuid`
#生成时间
curDate=`date +%Y-%m-%d_%H_%M_%S`
#创建文件夹
dirpath='/tmp/'$domain'__'$curDate'___'$uuid'/'
mkdir $dirpath

echo "start to execute weakfilescan/wyspider.py script"
cd weakfilescan
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
