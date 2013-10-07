#!/bin/bash

root=/home/yipeiw/Documents/baseline

tool=$root/Train/ToArffFormat.py

ftrfile=$root/Train/feature.txt

trainfile=$root/Train/data/train10test5/train-10.txt
outputPath=$root/Train/data/arff/train10test5
mkdir -p $outputPath

#$tool $trainfile $ftrfile $outputPath

testfile=$root/Train/data/train10test5/test-5.txt
$tool $testfile $ftrfile $outputPath
