#!/usr/bin/env python3

### trialParser.py
# author: Yiyun Zhao
# created: May 2019
# last modified by: Yiyun
# last modified on: 2019-May-21

import csv
from collections import defaultdict, OrderedDict
#from backstage import MicrophoneCheck as MC
#from backstage import errors, blockParser

# parse the study Specification file into blocks 

study_details = None

def readCSV(StudySpecification):
	with open(StudySpecification,newline = '') as csvfile:
		studySpec = list(csv.reader(csvfile))
	return studySpec

def readStduy(study_input_file):
	"""FUNC: parse the rows study_specification.csv into their corresponding blocks"""
	'''
	Input: study_input_file.csv
	Output: a squence of blocks which has the row within it. [Block1, Block2]; Block = {'name','repeat','type','lingUnit','stimuli'}
	'''
	studyInfo = {}

	BlockInformation = OrderedDict()
	currentblock = None
	StudyInput = readCSV(study_input_file)

	# the meta info line: 
	# line 1 & line 2 (study type)
	study_details = StudyInput[0][:3]
	studyInfo['Details'] = study_details
	#Session, List, Grammar = BlockInformation['Details']
	studyInfo['Type'] = StudyInput[1][0]
	#BlockInformation['StudyType'] = [StudyInput[1][0]]

	for rowinx, content in enumerate(StudyInput[2:]):
		if not content[0].startswith('#') and content[0]:
			head = content[0].lower()
			if head.startswith('welcome') or head.startswith('comments') or head.startswith('speak') or \
			head.startswith('learn') or head.startswith('survey') or head.startswith('understand'):
				block = head
				BlockInformation[block] = [content]
			else:
				BlockInformation[block].append(content)
	studyInfo['Blocks'] = BlockInformation

	return studyInfo

			




