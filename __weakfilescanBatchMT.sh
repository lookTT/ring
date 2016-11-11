#!/bin/bash

#获取绝对路径地址参数
filefullpath=$(readlink -f $1)
infile=$(readlink -f $2)
outfile=
if [ ! -n "$3" ] ;then
    outfile="log_weakfilescanMT.out"
else
    outfile=$3
fi
echo "the output file is $outfile"


nohup sh __weakfilescanMT.sh $filefullpath $infile > $outfile  2>&1 &

echo "__weakfilescanBatchMT Done"
