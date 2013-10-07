#!/bin/bash

root=/home/yipeiw/Documents/baseline

tool=$root/Train/DataSeparation.py

filelist=$root/metaData/ftrfile.list
outputPath=$root/Train/data/train10test5
mkdir -p $outputPath

$tool $filelist $outputPath
