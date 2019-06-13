import csv, os
from collections import defaultdict
from backstage import stimuli, responses, trialTemplates, procedure

directory = os.path.join('backstage')

def read(MIC):
    with open(MIC, 'rU') as inCSV:
        inReader = csv.reader(inCSV, dialect='excel', delimiter=',')
        check = list(inReader)
    return check

def splitter(cell):
    if ', ' in cell: content = cell.split(', ')
    elif ',' in cell: content = cell.split(',')
    else: content = cell

    return content

def numerizer(content_item):
    try: float(content_item)
    except ValueError: pass
    else:
        if float(content_item).is_integer(): content = int(content_item)
        else: content = float(content_item)

    return content


def create_trials(row, headers, cover_trials, trial_templates, end_trials):
	#print(row)
	t_name, t_type, t_stimuli, stim_locations, t_responses, t_delay, stim_text = row
	trial_templates.append(t_name)
	
	# process numeric column valuesif stim_locations:
	stim_locations = splitter(stim_locations)
	for c in range( len(stim_locations) ):stim_locations[c] = numerizer(stim_locations[c])
	if t_delay: t_delay = numerizer(t_delay)

	t_stimuli= t_stimuli.split(',')

	instr_name, image_name = t_stimuli
	stimuli.text(instr_name,stim_text)
	stimuli.image(image_name,content = 'alien_say1.png',width='70%')
	trialTemplates.instruction(t_name,[[image_name+'_img',instr_name+'_text']])

def process(text_check):
	cover_trials, trial_templates, end_trials = [], [], []
	for row in text_check:
		if row == '' or row == []: 
			continue
		elif row[0] == 'name':
			headers=row
		else:
			create_trials(row,headers,cover_trials,trial_templates,end_trials)
	procedure.block(['TextCheck','',[],'',False], cover_trials, trial_templates, end_trials, order = 'fixed')
	#procedure.block_seq=seq

def create(check_type):
	Text = os.path.join(directory, check_type)
	text_check = read(Text)
	process(text_check)




