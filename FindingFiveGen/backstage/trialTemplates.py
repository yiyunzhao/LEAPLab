#!/usr/bin/env python3

### trialTemplates.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Noah
# last modified on: 2018-11-06

""" Handle trial template objects and output file for a FindingFive study """

from backstage import FindingFiveObjectClasses as FF, reformat

template_objects = {}   # trial template objects (used to populate TrialTemps)

def instruction(name, content, **kwargs):
    tt = FF.InstrTemplate() # all instructions require unique objects
    tt.name = name
    try: tt.stimuli = content
    except: tt.stimuli = [['Alien', content]]
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt


def exposure(name, stimuli, needs_text, **kwargs):
    # exposure templates can handle multiple trials
    if name not in template_objects.keys(): # only create if first occurrence
        tt = FF.ExpTemplate()
        tt.name = name
        tt.stimuli = []
        tt.responses = []
        if 'Sent' in name: tt.delay = 1
        tt.force_response_delay = "passive"
    else: tt = template_objects[name]
    
    # whether or not the template is new, handle text as needed
    new_stims = []
    if needs_text == True:
        au = stimuli.pop()
        tx = au.replace('aud','text')
        stimuli.extend([au, tx])
        new_stims.append({'which':stimuli, 'location':[2,1,5]})
    else: new_stims = stimuli
    tt.stimuli.extend(new_stims)
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt


def comprehension(name, stimuli, response, needs_text, **kwargs):
    tt = FF.CompTemplate()
    tt.name = name
    tt.stimuli = stimuli
    tt.responses = [response]
    tt.force_response_delay = "passive"
    if needs_text == True:
        au = stimuli.pop()
        tx = au.replace('aud','text')
        tt.stimuli = []
        tt.stimuli.append({'which':[au, tx], 'location':[1,2]})
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt


def production(name, stimuli, response, needs_text, **kwargs):
    # production templates can handle multiple trials
    if name not in template_objects.keys(): # only create if first occurrence
        tt = FF.ProdTemplate()
        tt.name = name
        tt.stimuli = []
        tt.responses = [response]
        if name.startswith('Sent'): tt.replayable = True
        
        if 'Noun' in name: tt.order = 'fixed'
        else: tt.order = 'random'
        
        tt.force_response_delay = "passive"

    else: tt = template_objects[name]
    # whether or not the template is new, handle text as needed
    new_stims = []
    
    if len(stimuli)>1: # sentences provide audio for verb
        if needs_text == True:
            au = stimuli.pop()
            tx = au.replace('aud', 'text')
            stimuli.extend([au, tx])
            new_stims.append({'which':stimuli, 'location':[5,1,2]})
        else: new_stims = stimuli
        tt.stimuli.extend(new_stims)
    else: # not a list, so append rather than extend
        new_stims = stimuli
        tt.stimuli.append(new_stims)
    
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt


def feedback(name, stimuli, needs_text, **kwargs):
    # feedback templates can handle multiple trials
    if name not in template_objects.keys(): # only create if first occurrence
        tt = FF.FeedBackTemplate()
        tt.name = name
        tt.stimuli = []
        tt.responses = []
    else: tt = template_objects[name]
    # whether or not the template is new...
    # [img,aud] --> [img,'Lumi_says',aud]
    stimuli.insert(1, 'Lumi_says')
    # handle text as needed
    if needs_text == True:
        au = stimuli.pop()
        tx = au.replace('aud', 'text')
        stimuli.extend([tx, au])
    # [img,'Lumi_says',aud] --> [img,'empty','Lumi_says',aud]
    else: stimuli.insert(1, 'empty')
    tt.stimuli.append({'which':stimuli, 'location':[2,5,8,1]})
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt


def create_final_comments_trial():
    tt = FF.TextRespTemplate()
    tt.name = 'Comments'
    tt.stimuli = []
    tt.responses = ['comment']
    template_objects[tt.name] = tt

def create_survey_trial(name,stimuli,response, **kwargs):
    if name not in template_objects.keys(): # only create if first occurrence
        tt = FF.ProdTemplate()
        tt.name = name
        tt.stimuli = []
        tt.responses = [response]
        tt.order = 'fixed'
        tt.force_response_delay = "passive"
    else: tt = template_objects[name]

    # stimuli
    tt.stimuli = stimuli

    # other settings
    for key, value in kwargs.items():
        setattr(tt, key, value)
    template_objects[name] = tt

def output(templates_file):
    global template_objects

    templates = list( sorted(template_objects.keys()) )
    FindingFiveTemps = {}
    for t in templates:
        o = template_objects[t]
        attributes = {}
        for att in dir(o):
            stim_pattern = {}
            if att.startswith('_') or att == 'name': continue
            if att == 'order' or att == 'repeat':
                stim_pattern[att] = getattr(o, att)
                attributes['stimulus_pattern'] = stim_pattern
                continue
            attributes[att] = getattr(o, att)
            continue
        if o.name == 'EndExp': # final instructions should not have a 'duration' parameter
            attributes.pop('duration')
        FindingFiveTemps[o.name] = attributes
        continue

    big_daddy = reformat.ffStr(FindingFiveTemps)
    big_daddy_formatted = reformat.txtStr(big_daddy)

    # Now write that file!
    with open(templates_file, 'w') as outputTXT:
        outputTXT.write(big_daddy_formatted)
