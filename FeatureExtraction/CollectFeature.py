#!/usr/bin/env python

import sys
from ParseStanfordNLP import *
import nltk.tree as NT
from collections import defaultdict

pairfile = sys.argv[1]
parserfile = sys.argv[2]
alignfile = sys.argv[3]
ftrfile = sys.argv[4]
idxfile = sys.argv[5]

def loadPairs(pairfile):
	fin = open(pairfile)
	head = fin.readline().strip()
	namelist = head.split(',')
	pair_list = []
	pair_map = {}
	while True:
		line = fin.readline()
		if not line:
			break
		linelist = line.strip().split(',')
		idx1,idx2,lb,text1,text2,name1,name2 = linelist[0:7]
		pair = {'ate':(idx1, name1, text1),'ana':(idx2, name2, text2), 'label':lb}
		pair['coref'] = {namelist[i]:linelist[i] for i in range(7, len(linelist))}
		pair_list.append(pair)
		pair_map[(idx1, idx2)] = pair

	fin.close()

	return pair_list, pair_map

def loadAlign(alignfile):
	align_dict = {}
	for line in open(alignfile):	
		linelist = line.strip().split(',')
		name, start, end = linelist[0:3]
		token_list = []
		for i in range(3, len(linelist)):
			tokenText = linelist[i]
			sentID, tokenID = tokenText[1:len(tokenText)-1].split()
			token_list.append( (int(sentID), int(tokenID)) )
		align_dict[name] = token_list
	return align_dict

def transformWordBound(name):
	return ['word_'+num for num in name[1:len(name)-1].split(':')]

def GetToken(name_list, align_dict):
	tok_list = []
	sent=0
	first = True
	for name in name_list:
		if not name in align_dict.keys():
			print "error capture ", name
			return [], 0
		for sentID, tokID in align_dict[name]:
			tok_list.append(tokID)
			if first:
				first=False
				sent=sentID
			else:
				if sentID != sent:
					return [], sent
	return sorted(tok_list), sent

def ExtractGrammar(parsed_sent, t):
	parseTree = NT.Tree.parse(parsed_sent['parse'])
	if max(t) > len(parseTree.pos()):
		print parsed_sent['parse']
		print "num leaves ", len(parseTree.pos())
		print t
	pathlist = parseTree.treeposition_spanning_leaves(min(t)-1, max(t))
	if len(t)==1:
		pos_list = parseTree.pos()
		tag = pos_list[t[0]-1][1]
	else:
		tag = parseTree[pathlist].node
	
	return len(pathlist), tag

def GetFeature(pair_list, align_dict, parsed_dict):
	data_dict = {}
	skiped = defaultdict(bool)
	for pair in pair_list:
		idx1, name1, text1 = pair['ate']
		idx2, name2, text2 = pair['ana']
		word1_name_list = transformWordBound(name1)
		word2_name_list = transformWordBound(name2)
		t1,s1 = GetToken(word1_name_list, align_dict)
		t2,s2 = GetToken(word2_name_list, align_dict)
		if len(t1)==0:
			skiped[idx1]=True
			print "skip %s %s %s %s" % (name1, text1, name2, text2)
			continue
		if len(t2)==0:
			skiped[idx2]=True
                        print "skip %s %s %s %s" % (name1, text1, name2, text2)
                        continue

		depth1, grammer1 = ExtractGrammar(parsed_dict[s1], t1)
		depth2, grammer2 = ExtractGrammar(parsed_dict[s2], t2)
		data_dict[(idx1, idx2)]=((depth1, grammer1), (depth2, grammer2))

	return data_dict, skiped

pair_list, pair_map = loadPairs(pairfile)
align_dict = loadAlign(alignfile)
parsed_dict = read_parser_result(parserfile)

data_dict,skiped = GetFeature(pair_list, align_dict, parsed_dict)
print "skiped ", len(skiped.keys())
 
fout = open(ftrfile, 'w')
f = open(idxfile, 'w')
fout.write("idx1,idx2,text1,text2,object_dist,word_dist,speaker_turns,dep1,grammer1,dep2,grammer2,label\n")

for pairIdx, localFtr in data_dict.items():
	pair = pair_map[pairIdx]
	ftr1 = localFtr[0]
	local1 = ",".join([str(ftr) for ftr in ftr1])
	ftr2 = localFtr[1]
	local2 = ",".join([str(ftr) for ftr in ftr2])
	cftr = ",".join(pair['coref'].values())

	idx1, name1, text1 = pair['ate']
	idx2, name2, text2 = pair['ana']
	label = pair['label']

	fout.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (idx1, idx2, text1, text2, cftr, local1, local2, label))	
	f.write("%s,%s,%s,%s,%s,%s,%s\n" % (idx1, idx2, name1, name2, text1, text2, label))

f.close()
fout.close()
