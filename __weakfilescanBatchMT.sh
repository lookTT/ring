#!/bin/bash

#获取绝对路径地址参数
filefullpath=$(readlink -f $1)
infile=$(readlink -f $2)

nohup sh __weakfilescanMT.sh $filefullpath $infile > "log_weakfilescanMT.out"  2>&1 &

echo "__weakfilescanBatchMT Done"
