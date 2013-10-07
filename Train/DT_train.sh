#!/bin/bash

root=/home/yipeiw/Documents/baseline
export CLASSPATH=$CLASSPATH:/home/yipeiw/Tool/weka-3-6-10/weka.jar
DT="java -Xmx1g weka.classifiers.trees.J48"

trainfile="$root/Train/data/arff/train10test5/train-10.arff"
testfile=$root/Train/data/arff/train10test5/test-5.arff
modelPath=$root/Train/model
mkdir -p $modelPath
modelfile="$modelPath/train10_DT.model"

logfile=train10_DT.log
log2=train10_test5.log

#echo "$DT -t $trainfile -x 5 -d $modelfile > $logfile"
#$DT -t $trainfile -x 5 -d $modelfile -i > $logfile
echo "$DT -T $testfile -l $modelfile -p 0>$log2"
$DT -T $testfile -l $modelfile -p 0 > $log2
