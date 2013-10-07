#!/usr/bin/env python

import sys
import os.path as path

import nltk.classify.weka as Weka

rawftrfile = sys.argv[1]
headfile = sys.argv[2]
outputPath = sys.argv[3]

def loadHead(headfile):
	ftrlist = []
	for line in open(headfile):
		ftrname, ftrtype = line.strip().split(':')
		ftrlist += [(ftrname, ftrtype)]
	return ftrlist 
	
#tag,idx1,idx2,text1,text2,object_dist,word_dist,speaker_turns,dep1,grammer1,dep2,grammar2,label
def loadData(filepath):
	data = []
	Idx_list = []
	fin = open(filepath)
	head = fin.readline()
	namelist = head.strip().split(',')
	while True:
		line = fin.readline()
		if not line:
			break
		linelist = line.strip().split(',')
		#tag, idx1, idx2, text1, text2
		Idx_list += [linelist[0:5]]
		feature_set = {namelist[i-1]:linelist[i] for i in range(5, len(linelist)-1)}
		label = linelist[len(linelist)-1]
		data += [(feature_set, label)]
	fin.close()
	return data, Idx_list

def WriteIdx(idxfile, ids):
	fout = open(idxfile, 'w')
	for item in ids:
		fout.write(",".join(item)+'\n')
	fout.close()


name = path.splitext(path.basename(rawftrfile))[0]

tokens, ids = loadData(rawftrfile)
ftr_list = loadHead(headfile)

formatter = Weka.ARFF_Formatter(['True', 'False'], ftr_list)

arfffile = path.join(outputPath, name + '.arff')
formatter.write(arfffile, tokens)

idxfile = path.join(outputPath, name + '.idx')
WriteIdx(idxfile, ids)

