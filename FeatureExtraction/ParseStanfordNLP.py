#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

def read_parser_result(filepath):
	sentence_dict={}
	tree = ET.parse(filepath)
	sentences=tree.getroot().find('document').find('sentences')
        for sentence in sentences:
        	sentenceID = int(sentence.get('id'))
		sentence_struct = {}
        	sentence_struct['parse'] = sentence.find('parse').text

            	tokens=sentence.find('tokens')
		token_list = {}
                for token in tokens:
                    	tokenID = int(token.get('id'))
                    	word = token.find('word').text
			lemma = token.find('lemma').text
			begin = token.find('CharacterOffsetBegin').text
			end = token.find('CharacterOffsetEnd').text
			POS = token.find('POS').text
			NER = token.find('NER').text
			token_struct={ \
				'lemma':lemma,\
				'start':int(begin),\
				'end':int(end),\
				'pos':POS,\
				'ner':NER}
			token_list[tokenID] = token_struct	
		sentence_struct['tokens']=token_list
		sentence_dict[sentenceID] = sentence_struct
	return sentence_dict
