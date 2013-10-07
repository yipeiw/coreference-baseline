#!/bin/bash

root=/home/yipeiw/Documents/baseline
tooldir=/home/yipeiw/Tool/stanford-corenlp-full-2013-06-20

inputfilelist=$root/preprocess/sentence/BySpeakerSent.list
config="tokenize,ssplit,pos,lemma,ner,parse,dcoref"

outputPath=$root/preprocess/ParseResult/BySpeaker
mkdir -p $outputPath

echo "java -cp $tooldir/stanford-corenlp-3.2.0.jar:stanford-corenlp-3.2.0-models.jar:xom.jar:joda-time.jar:jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators $config -filelist $inputfilelist -outputDirectory $outputPath -replaceExtension"

java -cp $tooldir/stanford-corenlp-3.2.0.jar:$tooldir/stanford-corenlp-3.2.0-models.jar:$tooldir/xom.jar:$tooldir/joda-time.jar:$tooldir/jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators $config -filelist $inputfilelist -outputDirectory $outputPath -replaceExtension
