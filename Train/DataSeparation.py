#!/usr/bin/env python

import sys
import os.path as path

ftrfilelist = sys.argv[1]
outputPath = sys.argv[2]

def WriteData(ftrain, data, tag):
	for sample in data:
		ftrain.write("%s,%s\n" % (tag, sample))

def signature(ftrfile):
	corename = path.splitext(path.basename(ftrfile))[0]
	return corename.split('_')[1]

def loadData(ftrfile):
	data = []
	fin = open(ftrfile)
	head = fin.readline()
	while True:
		line = fin.readline()
		if not line:
			break
		data.append(line.strip())
	fin.close()
	return data, head

trainfile = path.join(outputPath, 'train-10.txt')
testfile = path.join(outputPath, 'test-5.txt')

train_num=10
count = 1
ftrain = open(trainfile, 'w')
ftest = open(testfile, 'w')
for line in open(ftrfilelist):
	ftrfile = line.strip()
	data, head = loadData(ftrfile)
	if count==1:
		ftrain.write(head)
		ftest.write(head)

	if count <= train_num:
		WriteData(ftrain, data, signature(ftrfile))
	else:
		WriteData(ftest, data, signature(ftrfile))
	count += 1

ftrain.close()
ftest.close()
