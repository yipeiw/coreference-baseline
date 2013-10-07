#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/baseline/preprocess/ExtractSentence.py

inputRoot=$root/data/CESAR
outputPath=$root/baseline/preprocess/sentence/BySpeaker
mkdir -p $outputPath

for subdir in $inputRoot/*;
do
	subname=$(basename $subdir)
	inputfile=$subdir/raw.xml
	outputfile=$outputPath/$subname.sent
	idxfile=$outputPath/$subname.idx
	echo "$tool $inputfile $outputfile $idxfile"
	$tool $inputfile $outputfile $idxfile
done
