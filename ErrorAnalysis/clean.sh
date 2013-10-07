#!/bin/bash

root=/home/yipeiw/Documents/baseline

tool=$root/ErrorAnalysis/CleanError.py

predict=$root/Train/train10_test5.log
testIdx=$root/Train/data/arff/train10test5/test-5.idx

FtrIdxPath=$root/metaData/featurefile

outputPath=$root/ErrorAnalysis/train10-test5-DT
mkdir -p $outputPath

outputfile=$outputPath/raw_test.error

$tool $predict $testIdx $FtrIdxPath $outputfile
