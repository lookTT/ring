#!/bin/bash

#判断参数个数是否正确
if [[ $# != 1 ]]; then
    echo "bad aparameterrg num: expect 1 get $#"
    exit
fi

#获取参数
filefullpath=$1
taskid=`uuid`

#读取文件 执行脚本
cat $filefullpath | while read myline
do 
    echo $myline
    nohup sh __weakfilescan.sh $myline $taskid > $myline".out"  2>&1 &
done


echo "Done"
