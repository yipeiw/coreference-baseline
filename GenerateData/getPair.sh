#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/baseline/GenerateData/GetCorefPair.py

pronounfile=$root/baseline/English_Pronoun.list

dataRoot=$root/data/CESAR
outputPath=$root/baseline/metaData/Pairs
mkdir -p $outputPath

for subdir in $dataRoot/*;
do
	subname=$(basename $subdir)
	objectfile=$subdir/object-reference.xml
	outputfile=$outputPath/$subname.pair
	echo "$tool $objectfile $outputfile $pronounfile"
	$tool $objectfile $outputfile $pronounfile
done
