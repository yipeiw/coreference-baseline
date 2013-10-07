#!/usr/bin/env python

import sys
from collections import defaultdict

from ParseStanfordNLP import *
parserfile = sys.argv[1]
utterfile = sys.argv[2]
featurefile = sys.argv[3]

def loadSentence(utterfile):
	count = 1
	sentence_dict=defaultdict(list)
	for line in open(utterfile):
		linelist = line.strip().split()
		for i in range(1, len(linelist)):
			text, name, pos = linelist[i].split('/')
			word = {'text':text, 'name':name, 'pos':int(pos)}
			sentence_dict[count] += [word]
		count += 1
	return sentence_dict

def GetWordRange(sentences):
	bound = {}
	lastPos = 0
	for idx, sentence in sorted(sentences.items(), key=lambda item:item[0]):
		for word in sorted(sentence, key=lambda item:item['pos']):
			bound[word['name']]=(lastPos, lastPos+len(word['text']))
			lastPos += len(word['text'])+1
		lastPos += 1
	return bound

def PlotTokenBound(sentence_dict):
	bar = {}
	first = True
	offset = 0
	for sent_id, sent_struct in sorted(sentence_dict.items(), key=lambda item:item[0]):
		for token_id, token in sorted(sent_struct['tokens'].items(), key=lambda item:item[0]):
			for i in range(token['start'], token['end']+1):
				bar[i] = (sent_id, token_id)
	return bar

def alignment(bound_dict, tokenTag, sentence_dict):
	word_align_dict = defaultdict(list)
	for word_id, bounds in bound_dict.items():
		(start, end) = bounds
		token_dict = defaultdict(bool)
		for n in range(start, end+1):
			token_dict[tokenTag[n]]=True
		for sentID, tokenID in token_dict.keys():
			t = sentence_dict[sentID]['tokens'][tokenID] #word, lemma, start, end, pos,ner
			if t['pos']=='.':
				continue #skip punctuation
			word_align_dict[word_id] += [(sentID, tokenID)]
	return word_align_dict


sentence_dict = read_parser_result(parserfile)
print "number of sentences ", len(sentence_dict.keys())
raw_sentence_dict = loadSentence(utterfile)

bound_dict = GetWordRange(raw_sentence_dict)
positionTag = PlotTokenBound(sentence_dict)
word_align_dict = alignment(bound_dict, positionTag, sentence_dict)
	
#part-of-speech, nerTag, (grammar function)
fout = open(featurefile, 'w')
for idx, elements in sorted(word_align_dict.items(), key=lambda item:int(item[0].split('_')[1])):
	tokens=["(%s %s)" % (item[0], item[1]) for item in elements]
	fout.write("%s,%s,%s,%s\n" % (idx, bound_dict[idx][0], bound_dict[idx][1],",".join(tokens)))
fout.close()
