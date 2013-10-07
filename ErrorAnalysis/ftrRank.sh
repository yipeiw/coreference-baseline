#!/bin/bash
root=/home/yipeiw/Documents/baseline
export CLASSPATH=$CLASSPATH:/home/yipeiw/Tool/weka-3-6-10/weka.jar

Rank="java weka.filters.supervised.attribute.AttributeSelection"
Eparam="weka.attributeSelection.InfoGainAttributeEval"

input=$root/Train/data/arff/train10test5/train-10.arff
output=$root/Train/data/arff/train10test5/train-10-IGselect.arff

echo "$Rank -E $Eparam -i $input -o $output -c last"
$Rank -E $Eparam -i $input -o $output -c last
