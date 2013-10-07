#!/bin/bash

root=/home/yipeiw/Documents/baseline

tool=$root/FeatureExtraction/WordTokenAlgin.py 

parsePath=$root/preprocess/ParseResult/BySpeaker
utterPath=$root/preprocess/sentence/BySpeaker
outputPath=$root/metaData/WordTokenAlign
mkdir -p $outputPath

for parsefile in $parsePath/*.xml;
do
	name=$(basename $parsefile)
	name=${name%*.*}
	utterfile=$utterPath/$name.idx
	ftrfile=$outputPath/$name.feat
	echo "$tool $parsefile $utterfile $ftrfile"
	$tool $parsefile $utterfile $ftrfile
done
