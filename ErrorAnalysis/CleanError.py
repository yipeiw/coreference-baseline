#!/usr/bin/env python

import sys
from collections import defaultdict
import os.path as path


predictfile = sys.argv[1]
testIdxfile = sys.argv[2]
idxPath = sys.argv[3]
outputfile = sys.argv[4]

def FindError(predictfile):
	error_list = []
	fin = open(predictfile)
	start = False
	while True:
		line = fin.readline()
		if not line:
			break
		if line.find('inst')!=-1:
			start=True
		if start:
			line = line.strip()
			if not line:
				break
			if line.find('+')!=-1:
				(idx,actual, predict, error, conf) = line.split()
				error_list += [(int(idx), actual, conf)]
	fin.close()
	return error_list

def loadInfo(testIdxfile):
	info_dict = {}
	count = 1
	for line in open(testIdxfile):
		doc,a1,a2,text1,text2=line.strip().split(',')
		info_dict[count]=(doc, int(a1), int(a2))
		count += 1
	return info_dict	

def map_info(error_list, info_dict):
	error_map = {}
	doc_dict = defaultdict(bool)
	for idx, actual, conf in error_list:
		doc_dict[info_dict[idx][0]]=True
		error_map[info_dict[idx]]=(idx, actual, conf)
	return error_map, doc_dict.keys()

def loadFtr(idxPath, doc_list):
	ftr_dict = {}
	for doc in doc_list:
		docpath = path.join(idxPath, 'CESAR_'+doc+'.idx')
		for line in open(docpath):
			(a1,a2,n1,n2,t1,t2,lb) = line.strip().split(',')
			ftr_dict[(doc, int(a1), int(a2))]=(n1, n2, t1, t2)
	return ftr_dict
	
def MapFeature(error_map, ftr_dict):
	error_data = {}
	for info, item in error_map.items():
		name1, name2, text1, text2 = ftr_dict[info]
		error_data[info] = item+ftr_dict[info]
	return error_data

error_list = FindError(predictfile)
info_dict = loadInfo(testIdxfile)
error_map, doc_list = map_info(error_list, info_dict)

ftr_dict = loadFtr(idxPath, doc_list)
error_data = MapFeature(error_map, ftr_dict)

error_name = defaultdict(bool)
fout = open(outputfile, 'w')
for info, ftr in sorted(error_data.items(), key=lambda item:(item[0][0], item[0][1])):
	(doc, a1, a2) = info
	(idx, actual, conf, name1, name2, text1, text2) = ftr
	error_name[text1]=True
	fout.write("%s,%s,%s,%s,%s,%s,%s\n" % (doc, text1, text2, name1, name2, actual, conf))
fout.close()

print "error names"
for name in error_name.keys():
	print name
