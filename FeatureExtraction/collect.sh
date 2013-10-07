#!/bin/bash

root=/home/yipeiw/Documents/baseline

tool=$root/FeatureExtraction/CollectFeature.py

PairPath=$root/metaData/Pairs
parsePath=$root/preprocess/ParseResult/BySpeaker
alignPath=$root/metaData/WordTokenAlign
outputPath=$root/metaData/featurefile
mkdir -p $outputPath

for pairfile in $PairPath/*.pair;
do
	name=$(basename $pairfile)
	name=${name%*.*}
	parsefile=$parsePath/$name.xml
	alignfile=$alignPath/$name.feat

	ftrfile=$outputPath/$name.ftr
	idxfile=$outputPath/$name.idx

	echo "$tool $pairfile $parsefile $alignfile $ftrfile $idxfile"
	$tool $pairfile $parsefile $alignfile $ftrfile $idxfile
done
