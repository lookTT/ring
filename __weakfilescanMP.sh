#!/bin/bash

#获取参数
domain=
infile=
uuid=`uuid`

#判断参数个数是否正确
if [[ $# -eq 2 ]]; then
    domain=$1
    infile=$2
elif [[ $#  -eq 3 ]]; then
    domain=$1
    infile=$2
    uuid=$3
else
    echo "bad aparameterrg num: expect 2or3 get $#"
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

filename='brutesearching.txt'
filefullpath=$dirpath$filename

echo "start to execute weakfilescan/brutesearching.py script"
cd ../weakfilescan
python brutesearching.py -d $domain -i $infile -o $filefullpath -t $uuid

echo "__weakfilescanMP Done"
