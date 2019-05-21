#! /usr/bin/env python3

### MicrophoneCheck.py
# author: Noah R Nelson
# created: February 2018
# last modified by: Noah
# last modified on: 2018-09-17

""" Read the appropriate mic check and create the FF objects to render it """

import csv, os
from collections import defaultdict
from backstage import stimuli, responses, trialTemplates, procedure

# directory holding the files is relative to FFEB_master
#directory = os.path.join('backstage', 'mic_check_files')
directory = os.path.join('backstage')

def read(MIC):
    with open(MIC, 'rU') as inCSV:
        inReader = csv.reader(inCSV, dialect='excel', delimiter=',')
        microphone_check = list(inReader)

    return microphone_check

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
    t_name, t_type, t_stimuli, stim_locations, t_responses, t_delay, stim_text = row

    # process trial template ordering
    if t_name in ['RecordInstr_preamble', 'RecordInstr_begin']: cover_trials.append(t_name)
    elif t_name == 'EndRecordPract': end_trials.append(t_name)
    else: trial_templates.append(t_name)

    # process numeric column values
    if stim_locations:
        stim_locations = splitter(stim_locations)
        for c in range( len(stim_locations) ):
            stim_locations[c] = numerizer(stim_locations[c])
    if t_delay: t_delay = numerizer(t_delay)

    # process stimuli
    t_stimuli = splitter(t_stimuli)
    if type(t_stimuli) is list:
        if t_type == 'instruction':
            instr_name, image_name = t_stimuli
            stimuli.text(instr_name, stim_text)
            stimuli.image(image_name, width = '50%')
        else:
            image_name, text_name = t_stimuli
            stimuli.text(text_name, stim_text, delay = t_delay)
            stimuli.image(image_name, content = 'alien_say1.png', width = '50%')
        t_stimuli = {'which':t_stimuli, 'location':stim_locations}
    else:
        stimuli.text(t_stimuli, stim_text)
        t_stimuli = [t_stimuli]

    # process responses and make templates
    if t_responses == 'voice': trialTemplates.production(t_name, t_stimuli, t_responses, needs_text = False, replayable = False, order = 'fixed')
    else: trialTemplates.instruction(t_name, t_stimuli)

def process(microphone_check):
    cover_trials, trial_templates, end_trials = [], [], []
    for row in microphone_check:
        # skip empty rows/content
        if row == '' or row == []: continue
        # ID headers and process trial rows
        if row[0] == 'name': headers = row
        else: create_trials(row, headers, cover_trials, trial_templates, end_trials)
    # make a block for the mic check
    procedure.block(['Mic_Check','',[],'',False], cover_trials, trial_templates, end_trials, order = 'fixed')
    #procedure.block_seq= seq
def create(check_type):
    mic_check = defaultdict(dict)
    MIC = os.path.join(directory, check_type)
    microphone_check = read(MIC)
    process(microphone_check)
