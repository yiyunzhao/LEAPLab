#!/usr/bin/env python3

### responses.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Noah
# last modified on: 2018-11-06

""" Create and build response objects for a FindingFive study """

import re
from backstage import FindingFiveObjectClasses as FF, reformat

response_objects = {}

def make_response_name_unique(my_response_name):
    response_names = response_objects.keys()
    if my_response_name in response_names:
        # name already exists. Append number, +1 until name is unique
        for i in range(1, 9):
            new_response_name = my_response_name + str(i)
            if new_response_name in response_names: continue
            else: return new_response_name
    else: return my_response_name

def voice():
    # we only need one voice object...
    if 'voice' in response_objects.keys(): return 'voice'
    # create an audio response object
    voice = FF.AudResponse()
    voice.name = 'voice'
    response_objects['voice'] = voice

    return 'voice'

def textbox(name = 'textbox', **kwargs):
    # usually only need one textbox object, but allow for others
    if name == 'textbox' and 'textbox' in response_objects.keys(): return 'textbox'
    # create a textbox response object
    textbox = FF.TextResponse()
    textbox.name = name
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(textbox, key, value)
    response_objects[name] = textbox

    return name

def create_final_comments_response():
    # we only need one comment object...
    if 'comment' in response_objects.keys(): return
    comment_box = FF.TextResponse()
    comment_box.name = 'comment'
    comment_box.instruction = 'If you have any comments you would like to leave about this HIT, please enter them below (limit {:d} characters).'.format(comment_box.max_char)
    comment_box.required = False
    response_objects['comment'] = comment_box


def create_AFC(choices,stimuli_nature,instruction,**kwargs):
    afc = FF.ChoiceResponse()
    afc.name = '_'.join(choices)
    afc.target = '%s:'+choices[0]
    afc.instruction = instruction
    afc.choices = ['%s:' + choice for choice in choices]

    for key, value in kwargs.items():
        setattr(afc, key, value)
    #response_objects[target] = afc
    response_objects[afc.name] = afc

    return afc.name



def create_AFCtext(target,choices,instruction,**kwargs):
    afc = FF.ChoiceResponse()
    afc.name = '_'.join(choices) + '_target_'+target
    afc.target = target
    afc.instruction = instruction
    afc.choices = choices
    afc.locations = 'fixed'

    for key, value in kwargs.items():
        setattr(afc, key, value)
    #response_objects[target] = afc
    response_objects[afc.name] = afc

    return afc.name



def create_4AFC(target, foils, **kwargs):
    afc = FF.ChoiceResponse()
    afc.name = target
    t = re.sub(r'\d+$', '', target) # remove digits at end of target
    afc.target = t.replace('4x','%s:') # replace '4x' with '%s' (clickable stim format)
    afc.instruction = 'Click on the image below that matches the word I say:'
    afc.choices = [afc.target]
    for foil in foils:
        foil = '%s:' + foil
        afc.choices.append(foil)
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(afc, key, value)
    response_objects[target] = afc

    return target

def create_2AFC(target, foil, **kwargs):
    afc = FF.ChoiceResponse()
    afc.name = target
    t = re.sub(r'\d+$', '', target) # remove digits at end of target
    afc.target = target.replace('2x','%s:')
    afc.choices = [afc.target, '%s:' + foil]
    afc.instruction = 'Click on the video that matches the sentence I say:'
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(afc, key, value)
    response_objects[target] = afc

    return target

def output(responses_file):
    # get set of attributes across all responses
    resp_headers = set()
    for n, o in response_objects.items():
        for attr in dir(o):
            if attr.startswith('_'): continue
            else: resp_headers.add(attr)
    resp_headers = list(resp_headers)
    resp_headers_formatted = reformat.jsonStr(resp_headers).replace('[', '').replace(']', '').replace(', ', ',')

    # set values for each attribute for each stimulus and push into a master list
    FindingFiveResps = []
    for name, response in response_objects.items():
        attrs = []
        for attr in resp_headers: # should be ORDERED set, so no issues with ordering
            try: attrs.append( getattr(response, attr) )
            except AttributeError:  attrs.append('')

        FindingFiveResps.append(attrs)

    csv_resps = reformat.jsonStr(FindingFiveResps)
    csv_resps_formatted = reformat.csvStr(csv_resps)

    # Now write that file!
    with open(responses_file, 'w') as outputTXT:
        outputTXT.write(resp_headers_formatted)
        outputTXT.write('\n')
        outputTXT.write(csv_resps_formatted)
