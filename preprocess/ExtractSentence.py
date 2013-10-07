#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Tool/iwsds_analysis_tools')

from read_write_annotation_files import *

import re
from collections import defaultdict


def Denoise(word):
	if word.find('%')!=-1 or word.find('<')!=-1 or word.find('>')!=-1:
		return ""
	return re.sub('\^|_|@','', word).strip()


transcript = sys.argv[1]
outputfile = sys.argv[2]
idxfile = sys.argv[3]

def TimeMerge(segments):
	refined = []
	used = defaultdict(bool)

	for n in range(0, len(segments)-2):
		if used[n]:
			continue
		speaker, merged_utter, merged_id_list, merged_s_time, merged_e_time =segments[n]
		for next_idx in range(n+2, len(segments), 2):
			Nspeaker, Nutter, next_id_list, next_s_time, next_e_time=segments[next_idx]
			if next_s_time > merged_e_time+1e-6:
				refined.append( (speaker, merged_utter, merged_id_list) )
				break
			else:
				used[next_idx]=True
				merged_utter += " "+Nutter
				merged_id_list += next_id_list
				merged_e_time = next_e_time 
	return refined


words, annotations, notes = read_annotation_file(transcript)

last_speaker=""
first=True
utterance = ""
segments = []
aveLen = 0
ID_list = []
utter_start = 0
utter_end = 0
word_list = []

for w in words:
	if first:
		last_speaker = w.speaker
		if Denoise(w.text)!='':
			utterance = Denoise(w.text) + ' ';
			ID_list=[(Denoise(w.text), w.name)]
			word_list=[w]
		first=False
	else:
		if last_speaker == w.speaker:
			if Denoise(w.text)!='':
                        	utterance += Denoise(w.text) + ' ';
                        	ID_list.append( (Denoise(w.text),w.name) )
				word_list.append(w)
		else:
			if utterance.strip() != "":
				s_time = word_list[0].s_time
				e_time = word_list[len(word_list)-1].e_time	
				segments += [(last_speaker, utterance.strip(), ID_list,s_time, e_time)]
				aveLen += len(utterance.split())

			last_speaker = w.speaker
                        ID_list = []
                        utterance = ""
			word_list = []
			if Denoise(w.text)!='':
                        	utterance = Denoise(w.text) + ' ';
                        	ID_list=[ (Denoise(w.text),w.name) ]
				word_list = [w]

refine_segments = TimeMerge(segments)
print "length of sentence %s, after merged:%s" % (len(segments), len(refine_segments))

count = 1
fout = open(outputfile, 'w')
f = open(idxfile, 'w')
for speaker, utter, id_list in refine_segments:
	fout.write("%s.\n" % (utter))

	outputText = ""
	for n in range(0, len(id_list)):
		outputText += "%s/%s/%s " % (id_list[n][0], id_list[n][1], n+1)
	f.write("<%s,%s> %s\n" % (count, speaker, outputText.strip()))
	count += 1
fout.close()
f.close()

print "ave sentence length %.3f" % (aveLen/count)
