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
#生成文件的绝对路径以及文件名
filename='wydomain_'$curDate'_'$uuid'.txt'
filefullpath='/tmp/'$filename

#开始执行域名及IP搜索
echo "start to execute wydomain script"
cd wydomain
python wydomain.py $1 $filefullpath
cd ../

#执行域名信息保存
cd wycommon
python wydomainSave2DB.py $uuid $1 $filefullpath
cd ../

#跑nmap相关
# cd wyportmap
# python 
# cd ../

#敏感信息泄露检测工具
# cd weakfilescan
# python
# cd ../