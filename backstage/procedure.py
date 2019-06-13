#!/usr/bin/env python3

### procedure.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Noah
# last modified on: 2018-11-06

""" Create block objects and build the procedure for a FindingFive study """

from backstage import FindingFiveObjectClasses as FF, reformat

block_seq = []
block_objects = {}

def block(info, covers, templates, ends, **kwargs):
    #name, repeat, label_info, feedback, needs_text = info
    name, repeat, ling_unit, feedback, needs_text = info
    b = FF.Block()
    b.name = name
    if repeat and int(repeat) > 1: b.repeat = int(repeat)
    b.cover_trials = covers
    b.trial_templates = templates
    b.end_trials = ends
    #if 'prod' in label_info and feedback == True:
    if name.lower().startswith("speak") and feedback == "FB":

        b.order = 'alternate'
    else: b.order = 'random'

    for key, value in kwargs.items():
        setattr(b, key, value)

    block_objects[name] = b
    return b

def create_final_comments_block():
    b = FF.Block()
    b.name = 'Comments'
    b.trial_templates = ['Comments']
    block_objects[b.name] = b
    return b


def output(procedure_file):
    global block_objects, block_seq

    blcks = list( sorted(block_objects.keys()) )
    FindingFiveBlocks = {}
    for b in blcks:
        o = block_objects[b]
        attributes = {}
        pattern = {}
        for att in dir(o):
            if att.startswith('_') or att == 'name': continue
            try:
                if getattr(o, att) in [[], '', {}]: continue
            except AttributeError: continue
            if att == 'order' or att == 'repeat':
                pattern[att] = getattr(o, att)
                attributes['pattern'] = pattern
                continue
            attributes[att] = getattr(o, att)
            continue
        FindingFiveBlocks[o.name] = attributes
        continue

    procedure = {
        'type': 'blocking',
        'blocks': FindingFiveBlocks,
        'block_sequence': block_seq
    }
    proc = reformat.ffStr(procedure)
    proc_formatted = reformat.txtStr(proc)

    # Now write that file!
    with open(procedure_file, 'w') as outputTXT:
        outputTXT.write(proc_formatted)
