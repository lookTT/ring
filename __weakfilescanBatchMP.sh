#!/bin/bash

#获取参数
filefullpath=$(readlink -f $1)
infile=$(readlink -f $2)
taskid=`uuid`

#读取文件 执行脚本
cat $filefullpath | while read myline
do 
    echo $myline
    nohup sh __weakfilescanMP.sh $myline $infile $taskid > $myline".out"  2>&1 &
done

echo "__weakfilescanBatchMP Done"
