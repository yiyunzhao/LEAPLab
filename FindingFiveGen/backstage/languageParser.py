#!/usr/bin/env python3

### languageParser.py
# author: Noah R Nelson, Yiyun Zhao
# created: September 2018
# last modified by: Yiyun 
# last modified on: 2019-May-21

# Major Modification:
# Change the data structure to Dictionary so the content relies on the precise keys rather than positions


"""
languageParser.py: parses the language input (language_input.csv)
"""

## REQUIRED MODULES
import csv

# globals
# this could be reached directly
nouns = {}
adjectives = {}
verbs = {}
adpositions = {}
case_markers = {}
word_orders = []
pp_types = []
pp_nom = []
Info = {}
LexiconTypeDic = {}

def main(language_input_file):
    with open(language_input_file, newline='') as inputCSV:
        inputReader = csv.reader(inputCSV, dialect='excel', delimiter=',')
        language_definition = list(inputReader)

    chunk = None # 'chunk' refers to the dictionary or grammar definition for this section of the input
    for row in language_definition:
        r = row[0].strip()
        # skip comments in the language input file
        if r.startswith('#'): continue
        # Get session, list, grammar details for cross-check w/ study input
        if r == 'DETAILS:':
            details = row[1:]
            continue
        # Identify end of current chunk (empty row)
        if r == '' or r is None: chunk = 'end'
        # Identify beginnings of new chunks
        if r.title() == 'Nouns': chunk = 'nouns'
        elif r.title() == 'Adjectives': chunk = 'adjectives'
        elif r.title() == 'Verbs': chunk = 'verbs'
        elif r.title() == 'Adpositions': chunk = 'adpositions'
        elif r.title() == 'Case Markers': chunk = 'case_markers'
        elif r.title() == 'Word Orders': chunk = 'word_orders'
        elif r.title() == 'Pp Types' or r.title() == 'Adposition Types': chunk = 'pp_types'
        elif r.title() == 'Pp Nom' or r.title() == 'Pp/Head Noun Orders': chunk = 'pp-headnoun_orders'
        # Get the content for the current chunk
        else:
            if (chunk == 'nouns'): nouns[r] = row[1]
            if (chunk == 'adjectives'): adjectives[r] = row[1]
            if (chunk == 'verbs'): verbs[r] = row[1]
            if (chunk == 'adpositions'): adpositions[r] = row[1]
            if (chunk == 'case_markers'): case_markers[r] = row[1]
            if (chunk == 'word_orders'): word_orders.append(r)
            if (chunk == 'pp_types'): pp_types.append(r)
            if (chunk == 'pp-headnoun_orders'): pp_nom.append(r)

    master_lexicon = {}
    lexicons = [nouns, verbs, adjectives, adpositions, case_markers]
    for dict in lexicons:
        for english, lumese in dict.items():
            master_lexicon[english] = lumese
    cm_positions = list( case_markers.keys() )


    # save study details for cross-check with other input file
    try:
        session_number = details[0][-1]
        list_number = details[1][-1]
        grammar_number = details[2][-1]
    except NameError: # if the csv is saved in Windows as UTF-8 encoded CSV, or "DETAILS:" is missing
        raise ( "Python can't read the language details. Check that {:s} is saved as basic (not UTF-8 encoded) CSV, with 'DETAILS:' written in the first column before the study details.".format(language_input) )

    grammar = {'word_orders': word_orders, 'pp_types': pp_types, 'cm_positions':cm_positions, 'pp_nom':pp_nom}
    lexicon = {'master_lexicon':master_lexicon, 'nouns': nouns, 'adjectives': adjectives, 'verbs':verbs,'adpositions':adpositions, 'case_markers':case_markers}
    # grammar = [word_orders,  pp_types, cm_positions, pp_nom]
    #lexicon = [master_lexicon, nouns, adjectives, verbs, adpositions, case_markers]


    #Update the LexiconTypeDic
    for k,v in lexicon.items():
        if k != 'master_lexicon' and len(v) > 1:
            for w in v:
                LexiconTypeDic[w] = k


    Info['details'] = details
    Info['grammar'] = grammar
    Info['lexicon'] = lexicon 


    return Info
