import re
from collections import OrderedDict
from backstage import errors, trialTemplates, stimuli, responses
#from backstage import processTrials
from backstage import lumese


#### Utilities #########
def getNumber(string):
	s = re.search(r'\d+', string)
	if s:
		return int(s.group())
	else:
		return ''

def getString(string):
    s = re.search(r'[A-Za-z]+', string)
    if s:
        return s.group()
    else:
        return ''

def normalizeLingUnit(string):
	lingUnit = ''
	if string.lower().startswith('noun'):
		lingUnit='Nouns'
	elif string.lower().startswith('verb'):
		lingUnit='Verbs'
	elif string.lower().startswith('phrase'):
		lingUnit = 'Phrases'
	elif string.lower().startswith('adjective'):
		lingUnit = 'Adjectives'
	elif string.lower().startswith('adposition'):
		lingUnit = 'Adpositions'
	elif string.lower().startswith('sentence'):
		lingUnit = 'Sentences'
	elif string.lower().startswith('mix'): # mix refers to the mix of the simple trials 
		lingUnit = 'Mix'
	else:
		raise Exception('invalid input LingUnit at block {' + block_name +'} either adding a new lingUnit in the normalizedLingUnit at trialParser.py or change the block lingUnit')
	return lingUnit


def bracnhesReform(branches):
	branchlist = branches.split(';')
	branchdict = OrderedDict()
	for b in branchlist:
		con, bs = b.split(":")
		con = ''.join(con.split())
		if bs.lower() in ['none','null','no','']:
			brans = []
		else:
			brans =[''.join(i.lower().split()) for i in  bs.split(',')]
		branchdict[con] = brans
	return branchdict


def conditionsReform(branches):
	branchlist = branches.split(';')
	branchdict = {}
	for b in branchlist:
		con, bs = b.split(":")
		con = ''.join(con.split())
		branchdict[con] = [bs]
	return branchdict

####### helper functions #################
def feedback_checker(trial,inputfeedback):
	# deal with feedback
	# globally specified feedback
	if inputfeedback:
		if inputfeedback.upper() == 'FB':
			feedback= True
		elif inputfeedback.upper() == "NFB":
			feedback = False
		else:
			raise Exception("feedback column H has undefined inputs, please select either FB or NFB.")
	else:
		feedback = False



	#feedback = bool(feedback)
	# if specified in line then overwrite the global one
	if trial[7]:
		if trial[7] == 'NFB':
			feedback = False
		elif trial[7] == 'FB':
			feedback = True
		else:
			raise Exception('Invalid input in the feedback column in line. Please select (NFB) or FB.')

	return feedback


def create_stimuli(name,trial,ling_unit,stimuli_nature,need_text,need_aud=True,promp=None):
	# three types of stimuli within a trial are possible
	vis, aud = None, None

	# simple vocabulary 
	if ling_unit in ['Nouns','Verbs','Adpositions','Adjectives','Mix']:
		content_vis = trial[0]
		if need_aud:
			content_lumese = lumese.SimpleWord(getString(content_vis),ling_unit.lower())
	
	# complex nouns
	elif ling_unit in ['Phrases']:
		content_vis = trial[0]
		if need_aud:
			try:
				PpType, PpNom = trial[5].split(',')
			except:
				raise Exception("Please Specify PpType, PpNom at line",name)
			content_lumese,_ = lumese.ComplexNoun(getString(content_vis),PpType=PpType,PpNom=PpNom)
	
	# sentences 
	elif ling_unit in ['Sentences']:
		content = trial[0:3]
		content_vis = '_'.join([i for i in content if i])
		wd_info, pp_info,case_info = trial[3], trial[5], trial[6]

		if need_aud:

			# get word order 
			if wd_info:
				wordorder = trial[3]
			else: 
				raise Exception('Sentence need word order specified!')
				
			# get the case information

			if case_info == 'NCM' or not case_info:
				case,position = None,None
				pass
			else:
				try:
					case,position = trial[6].split(',')
				except:
					raise Exception('Please specify case information: \n 1. case on which element \n 2. suffix or prefix \n in this format:SNOUN,suffix')

			# get the preposition type if there is one
			if not pp_info:
				PpType,PpNom = None, None
			else:
				try:
					PpType, PpNom = trial[5].split(',')
				except:
					raise Exception('Please specify complete adposition information: \n 1. preposition or postposition \n 2. prenominal or postnominal')
			clean_content = [getString(i) for i in content]
			content_lumese,_ = lumese.Sentence(clean_content,wordorder,case,position,PpType,PpNom)
	else:
		raise Exception('Undefined ling_unit found, please select among (nouns,verbs,adpositions,adjectives,mix,phrase,sentences).')

	# visual stimuli:
	if not stimuli_nature:
		pass
	elif stimuli_nature == 'image':
		vis = stimuli.image(content_vis)
	elif stimuli_nature == 'video':
		vis = stimuli.video(content_vis)
	else:
		raise Exception('Invalid visual stimuli nature: (image or video)')

	# audio stimuli
	if need_aud:
		aud = stimuli.audio(content_lumese, need_text)
	else:
		pass

	# collect the non-None stimuli
	stim_collection = []
	if vis:
		stim_collection.append(vis)
	if aud:
		stim_collection.append(aud)


	if promp: # promp currently is limited to the simple words
		promp_lumese = lumese.SimpleWord(getString(promp),"Mix")
		promp_aud = stimuli.audio(promp_lumese,need_text)
		stim_collection.append(promp_aud)
	return stim_collection

def create_choices(name,indx,trial,ling_unit,stimuli_nature,feedback, **kwargs):
	feedback = feedback_checker(trial,feedback)
	vid = []
	foils = []
	if ling_unit in ["Sentences"]:
		target =  '_'.join([i for i in trial[0:3] if i]) 
		foils = trial[9].split(";")

	else:
		target= trial[0]
		if trial[9]: 
			foils = trial[9].split(";")
		else:
			foils = trial[1:5]

	foils = [i for i in foils if i]

	if not foils:
		raise Exception('No foils specified in column J! for block '+ name+' row '+ str(indx+1))
	vid.append(target)
	vid+=foils


	response_collection = None
	stim_collection =[]
	if stimuli_nature == 'image':
		for i in vid:
			vis = stimuli.image(i)
			stim_collection.append(vis)
		instruction = 'Click on the image below that matches the word I say:'
		response_collection = responses.create_AFC(stim_collection, stimuli_nature,instruction,feedback=feedback,**kwargs)

	elif stimuli_nature == 'video':
		for i in vid:
			vis = stimuli.video(i)
			stim_collection.append(vis)
		instruction = 'Click on the video below that matches the word I say:'
		response_collection = responses.create_AFC(stim_collection, stimuli_nature,instruction,feedback=feedback,**kwargs)
	else:
		raise Exception('Invalid visual stimuli nature: (image or video)')

	return response_collection


def instruction(name, content):
	stim = stimuli.Alienlumi()
	instr_stimulus = stimuli.text(name, content) # creates the stimulus object
	template_name = name.replace('Instr','_instr') + '_Trial'
	trialTemplates.instruction(template_name, instr_stimulus) # creates the trial template object
	return template_name


#######################################
#		Experimental BLOCKS			  #
#######################################

#---------- comment block-------------#
def comments():
	responses.create_final_comments_response()
	trialTemplates.create_final_comments_trial()
	procedure.create_final_comments_block()

#---------- welcome block ------------#
def welcome(content,name,need_text,**kwargs):

	# intialize elements
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, foil, _, _, feedback = content[0][:8]
	block_info = [name, repeat, ling_unit, feedback, need_text]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)


	## process the contents:
	for indx,content in enumerate(content[1:]):
		instr_content = content[1]
		instr_name = name + 'Instr'+ str(indx+1)
		my_instr_template = instruction(instr_name, instr_content)
		main.append(my_instr_template)
	return block_info, cover, main, end,branch_info

#---------survey block-------------#
def AFCsurvey(content,name,need_text,**kwargs):
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, foil, _, _, feedback = content[0][:8]
	block_info = [name, repeat, ling_unit, feedback, need_text]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)

	# process trials
	choices_templates = []
	triggers = []
	branches = {}
	for indx, trial in enumerate(content[1:]):

		# create instruction cover trials 
		if trial[0].lower().startswith('instr'):
			instr_content = trial[1]
			instr_name = name + 'Instr'+ str(indx+1)
			my_instr_template = instruction(instr_name, instr_content)
			
			if indx < len(content[1:])/2:
				cover.append(my_instr_template)
			else:
				end.append(my_instr_template)
		
		elif trial[0].lower().startswith('end'):
			pass

		else:
			# create main trial stimuli (which does not contain the visual stimuli)
			question_name,question_content,choices,target = trial[0],trial[1],trial[2],trial[3]
			trig, condition = trial[11],trial[12]
			#this_trial_name = '_'.join([name,'trial',str(indx),question_name])
			question_name = '_'.join([name,question_name])
			question_simulus = stimuli.text(question_name,question_content)
			question_response = responses.create_AFCtext(target,choices.split(','),instruction='please select the answer that fits your situation',feedback=False)
			trialTemplates.create_AFCsurvey_trial(question_name, [question_simulus], question_response)
			main.append(question_name)



			# updating the trigger information
			if trig:
				triggers.append({"trial_template":question_name, "response":question_response})

			if condition:
				contrans = conditionsReform(condition)
				for key, val in contrans.items():
					if key in branches:
						branches[key]+= val
					else:
						branches[key] = val
	
	if triggers or branches:
		branch_info.append(triggers)
		branch_info.append(branches)

	return block_info, cover, main, end, branch_info


def survey(content,name,need_text,**kwargs):
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, foil, _, _, feedback = content[0][:8]
	block_info = [name, repeat, ling_unit, feedback, need_text]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)
	

	# process the stimuli 
	survey_stimuli = []
	triggers_collection = []
	for indx, trial in enumerate(content[1:]):

		# create instruction cover trials 
		if trial[0].lower().startswith('instr'):
			instr_content = trial[1]
			instr_name = name +ling_unit+'Instr'+ str(indx+1)
			my_instr_template = instruction(instr_name, instr_content)
			
			if indx < len(content[1:])/2:
				cover.append(my_instr_template)
			else:
				end.append(my_instr_template)
		
		elif trial[0].lower().startswith('end'):
			pass
		# create main trial stimuli (questions)
		else:
			question_name,question_content = trial[0],trial[1]
			question_name = '_'.join([name,question_name])
			question_simulus = stimuli.text(question_name,question_content)
			survey_stimuli.append(question_simulus)
			trigger,condition = trial[10],trial[11]

	# create trial name 
	survey_template_name = name +'_Questions_Trial'
	main.append(survey_template_name)

	# trial response 
	response = responses.textbox()

	# trial survey trials 
	trialTemplates.create_survey_trial(survey_template_name,survey_stimuli,response,**kwargs)
	return block_info, cover, main, end,branch_info

#----------learn block------------------#
def learn(content,name,need_text,**kwargs):
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, _, _, _, feedback = content[0][:8]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)
	
	
	# normalized the information
	repeat = getNumber(repeat) # get the number out
	ling_unit = normalizeLingUnit(ling_unit)
	block_info = [name, repeat, ling_unit, feedback, need_text]



	# process trials 
	# create trial name 
	learn_template_name = '_'.join([name,ling_unit,'trial'])
	for indx, trial in enumerate(content[1:]):
		# create instruction cover trials 
		if trial[0].lower().startswith('instr'):
			instr_content = trial[1]
			instr_name = name + 'Instr'+ str(indx+1)
			my_instr_template = instruction(instr_name, instr_content)
			
			if indx < len(content[1:])/2:
				cover.append(my_instr_template)
			else:
				end.append(my_instr_template)
		
		elif trial[0].lower().startswith('end'):
			pass

		else:
			# create main trial stimuli (questions)
			this_trial_stimuli = create_stimuli(name,trial,ling_unit,stimuli_nature, need_text)

			# create trial templates and no response needed
			trialTemplates.exposure(learn_template_name,this_trial_stimuli,need_text)
	main.append(learn_template_name)
	return block_info, cover, main, end, branch_info


#--------------- Comprehension Block --------------#
def understand(content,name,need_text,**kwargs):
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, foil, _, _, feedback = content[0][:8]

	# normalized the information
	repeat = getNumber(repeat) # get the number out
	ling_unit = normalizeLingUnit(ling_unit)
	block_info = [name, repeat, ling_unit, feedback, need_text]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)

	# process trials
	understand_templates = []
	triggers = []
	branches = {}
	for indx, trial in enumerate(content[1:]):

		# create instruction cover trials 
		if trial[0].lower().startswith('instr'):
			instr_content = trial[1]
			instr_name = name + 'Instr'+ str(indx+1)
			my_instr_template = instruction(instr_name, instr_content)
			
			if indx < len(content[1:])/2:
				cover.append(my_instr_template)
			else:
				end.append(my_instr_template)
		
		elif trial[0].lower().startswith('end'):
			pass

		else:
			# create main trial stimuli (which does not contain the visual stimuli)
			this_trial_name = '_'.join([name,ling_unit,'trial',str(indx),trial[0]])
			trig, condition = trial[11],trial[12]
			this_trial_stimuli = create_stimuli(name,trial,ling_unit, None, need_text)
			this_trial_response = create_choices(name,indx,trial,ling_unit,stimuli_nature,feedback=feedback)
			trialTemplates.comprehension(this_trial_name, this_trial_stimuli, this_trial_response,need_text)
			main.append(this_trial_name)


						# updating the trigger information
			if trig:
				triggers.append({"trial_template":this_trial_name, "response":this_trial_response})

			if condition:
				contrans = conditionsReform(condition)
				for key, val in contrans.items():
					if key in branches:
						branches[key]+= val
					else:
						branches[key] = val
	
	if triggers or branches:
		branch_info.append(triggers)
		branch_info.append(branches)

	return block_info, cover, main, end, branch_info


#--------------- Production Block --------------#
def speak(content,name,need_text,**kwargs):
	cover, main, end = [],[],[]
	branch_info = []
	_, repeat, ling_unit, stimuli_nature, foil, _, _, feedback = content[0][:8]

	# normalized the information
	repeat = getNumber(repeat) # get the number out
	ling_unit = normalizeLingUnit(ling_unit)
	block_info = [name, repeat, ling_unit, feedback, need_text]

	#branch_status
	if content[0][11]: 
		branch_info.append(content[0][11])
	if content[0][12]:
		branch_info.append(content[0][12].split(':'))
	if content[0][13]:
		branches = bracnhesReform(content[0][13])
		branch_info.append(branches)


	# process trials
	# trial name
	produce_template_name = '_'.join([name,ling_unit,'trial'])
	speak_templates = []
	for indx, trial in enumerate(content[1:]):

		# create instruction cover trials 
		if trial[0].lower().startswith('instr'):
			instr_content = trial[1]
			instr_name = name + 'Instr'+ str(indx+1)
			my_instr_template = instruction(instr_name, instr_content)
			
			if indx < len(content[1:])/2:
				cover.append(my_instr_template)
			else:
				end.append(my_instr_template)
		
		elif trial[0].lower().startswith('end'):
			pass

		else:
			# create main trial stimuli (which does not contain the visual stimuli)
			this_trial_promp = trial[10] # change the position, origin is trial[3]
			this_trial_stimuli = create_stimuli(name,trial,ling_unit,stimuli_nature,need_text,promp=this_trial_promp)
			speak_templates.append(this_trial_stimuli)
			#feedback = feedback_checker(trial,feedback)
			target_aud = this_trial_stimuli.pop(1)
			# response
			if need_text:
				this_trial_response = responses.textbox()
			else:
				this_trial_response = responses.voice()

			# trial template
			trialTemplates.production(produce_template_name, this_trial_stimuli, this_trial_response,need_text,**kwargs)

			if feedback_checker(trial,feedback) == True:
				stimuli.lumi()
				feedback_audio= stimuli.feedback(target_aud,need_text)
				target_image = this_trial_stimuli[0]
				feedback_template = '{}Feedback'.format(produce_template_name)
				trialTemplates.feedback(feedback_template, [target_image, feedback_audio], need_text)


	# create trials
	main.append(produce_template_name)
	if feedback_checker(trial,feedback) == True:
		main.append(feedback_template)
	
	return block_info, cover, main, end, branch_info















	
	














