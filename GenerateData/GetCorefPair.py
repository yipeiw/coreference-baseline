#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Tool/iwsds_analysis_tools')

from read_write_annotation_files import *
import nltk
import time

import re

from collections import defaultdict

def Denoise(word):
        if word.find('%')!=-1 or word.find('<')!=-1 or word.find('>')!=-1:
                return ""
        return re.sub('\^|_|@','', word).strip()

def PostProcessAnnotation(annotations):
	correct = []
	for i in range(0, len(annotations)):
		ai = annotations[i]
		ai.number = i
		ai.words = sorted(ai.words, key=lambda item:int(item.name.split('_')[1]))
		correct.append(ai)
	return correct


objectfile = sys.argv[1]
pairfile = sys.argv[2]
pronounfile = sys.argv[3]

def LoadPronoun(filepath):
	candidate_list = defaultdict(int)
	for line in open(filepath):
		linelist = line.strip().split(',')
		if linelist[len(linelist)-1].find('PT')!=-1:
			PT = int(linelist[len(linelist)-1].split(':')[1])
			if PT==1 or PT==2:
				candidate_list[linelist[0].lower()]=1
				continue

		candidate_list[linelist[0].lower()]=2
	return candidate_list


def GetWord(word_list):
	word_ids = []
	Text = ""
	for word in sorted(word_list):
		if Denoise(word.text)!="":
			Text += Denoise(word.text) + ' '
			word_ids.append(word.name.split('_')[1])
	return Text.strip(), word_ids


def IsPronoun(word, resource, kind):
	if kind=="dict":
		tokens = nltk.tokenize.word_tokenize(word)
		norm_word = tokens[0].lower()
		return resource[norm_word]
	elif kind=="tag":
		#to do	
		return True
	else:
		print "kind error ", kind
		return False

def SpeakerTurns(wordStart, wordEnd, word_map):
	speakers = 0
	first = True
	pre = ""
	for nWord in range(wordStart+1, wordEnd):
		if first:
			first=False
			current = word_map['word_'+str(nWord)]
			continue
		pre=current
		current = word_map['word_'+str(nWord)]
		if current.speaker!=pre.speaker:
			speakers += 1
	return speakers

def ExtractCorefFtr(aPre, ai, word_map):
	text1, ids1 = GetWord(aPre.words)
	text2, ids2 = GetWord(ai.words)
	range1 = sorted([int(idx) for idx in ids1])
	range2 = sorted([int(idx) for idx in ids2])
	word_interval = min(range2)-max(range1)
	return [ai.number-aPre.number, word_interval, SpeakerTurns(max(range1), min(range2), word_map)]

	
def GeneratePair(word_map, annotations, precede, current):
	pairs = []
	for n in range(0, len(precede)):
		if precede[n]==0:
			a_candidate = annotations[n]
			ai = annotations[current]
			lb = (a_candidate.object_parameter==ai.object_parameter)
			pairs += [(n, current, lb, ExtractCorefFtr(a_candidate, ai, word_map))]
	return pairs

pronoun_list = LoadPronoun(pronounfile)
print pronoun_list

words, annotations, notes = read_annotation_file(objectfile)
annotations = PostProcessAnnotation(annotations)
word_map = {word.name:word for word in words}
print "initialize succeed ", len(annotations)

startTime = time.time()
pairList = []
precede = []
num_pro = 0
for n in range(0, len(annotations)):
	ai = annotations[n]
	#tag = IsPronoun(ai.words, POS_dict, 'tagger')
	word_text = " ".join([Denoise(word.text) for word in ai.words])
	if word_text=="":
		precede.append(3)
		continue
	tag = IsPronoun(word_text.strip(), pronoun_list, 'dict')
	if tag==2:
		num_pro += 1
		pairList += GeneratePair(word_map, annotations, precede, n)
	precede.append(tag)

print "complete generation ", time.time()-startTime
print "number of pro ", num_pro

fout = open(pairfile, 'w')
fout.write("object1,object2,label,text1, text2,wordnames1, wordnames2,object_dist,word_dist,speaker_turns\n")
for idx1, idx2, lb, ftr_list in pairList:
	ai=annotations[idx1]
	aj=annotations[idx2]
	words1, word1_ids = GetWord(ai.words)
	words2, word2_ids = GetWord(aj.words)

	word_name1=":".join(word1_ids)
	word_name2=":".join(word2_ids)

	ftrline=",".join([str(ftr) for ftr in ftr_list])

	fout.write("%s,%s,%s,%s,%s,<%s>,<%s>,%s\n" % (idx1, idx2, lb, words1, words2, word_name1, word_name2, ftrline))

fout.close()
