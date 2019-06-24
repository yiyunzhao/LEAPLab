import csv
from collections import defaultdict, OrderedDict
from backstage import MicrophoneCheck as MC
from backstage import TextCheck as TC
from backstage import studyParser as SP
from backstage import trialParser as TP
from backstage import procedure
#from backstage import errors, blockParser

#### FUNC ####
"""
Input: blockinformation from study_processor (Dictionary)
Output:
	Initialize the FFobjects of block objects; trial objects; stimuli objects and response objects
"""
def process_blockType(study_type,study_details,study_block):
	print(study_type,study_details)
	
	# initial variables
	need_text = False
	block_sequence = []



	# deal with the study type (automatically generated the related stimuli, responses, trials, blocks information)
	if study_type.title().startswith('Text'):
		need_text = True
		TC.create('TextCheck.csv')
		block_sequence.append('TextCheck')
	elif study_type.title().startswith('Mic'):
		session_num = int(study_details[0].split()[-1])
		if session_num>=2:
			mt = 'MicCheck2.csv'
			block_sequence.append('MicCheck2')
		else:
			mt = 'MicCheck.csv'
			block_sequence.append('MicCheck')
		MC.create(mt)        
	else:
		raise Exception('Study Type is not correctly specified') 


	# process the study blocks
	for block_key,block_value in study_block.items():
		block_name = ''.join(block_key.split())
		
		# diverge the blocks into different levels of processing based on the block_nature and stimuli
		# this can be modified for adding new block type, but be sure to create new trial templates for this block as well


		# block_info: [name,repeat,label_info, feedback,needs_text]

		# this block is used for greeting and general indsturctions
		if block_name.lower().startswith("welcome"):
			#print(block_value)
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.welcome(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info)
			## generate related trials using the information here welcome(block_contents)

		# this block is used for comments
		elif block_name.lower().startswith('comm'):
			block_info = []
			TP.comments()
			#block_info, cover_trials, main_trials, end_trials = TP.comment(block_value,block_name,need_text)
			#print(block_value)

		# this block is used for surveys
		elif block_name.lower().startswith('surv'):
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.survey(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info,order='fixed')
			#print(block_value)

		elif block_name.lower().startswith('afcsurv'):
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.AFCsurvey(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info,order='fixed')

		# this block is used for training
		elif block_name.lower().startswith("learn"):
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.learn(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info)
			#print(block_value)

		# this block is used for comprhension (AFC)
		elif block_name.lower().startswith('understand'):
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.understand(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info)
			#print(block_value)

		elif block_name.lower().startswith('speak'):
			block_info, cover_trials, main_trials, end_trials,branch_info = TP.speak(block_value,block_name,need_text)
			procedure.block(block_info, cover_trials, main_trials, end_trials,branch_info)
			#print(block_value)

		else:
			raise Exception('Study block type is not correctly defined. \n Current allowed block types include: welcome, comments, survey,learn,understand,speak')



		if not branch_info:
			block_sequence.append(block_name)
		elif branch_info[0].lower().startswith('sub'):
			continue
		elif branch_info[0].lower().startswith('branch'):
			block_sequence.append(block_name)
			block_sequence.append(dict(branch_info[2]))
		else:
			raise ValueError("undefined block status")


	# update block_sequence
	procedure.block_seq = block_sequence



def blockProcessor(studyInfo):
	study_details, study_type,study_block = studyInfo['Details'],studyInfo['Type'],studyInfo['Blocks']
	process_blockType(study_type,study_details,study_block)


		











