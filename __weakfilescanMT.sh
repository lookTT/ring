#!/bin/bash

filefullpath=
infile=
taskid=`uuid`

#判断参数个数是否正确
if [[ $# -eq 2 ]]; then
    filefullpath=$1
    infile=$2
elif [[ $# -eq 3 ]]; then
    filefullpath=$1
    infile=$2
    taskid=$3
else
    echo "bad aparameterrg num: expect 2or3 get $#"
    exit
fi

#读取文件 执行脚本
cat $filefullpath | while read myline
do 
    echo $myline
    sh __weakfilescanMP.sh $myline $infile $taskid
done

echo "__weakfilescanMT Done"
