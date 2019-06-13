#!/usr/bin/env python3

### motherboard.py
# author: Noah R Nelson
# created: December 2017
# last modified by: Noah
# last modified on: 2018-12-17






"""
Motherboard.py: read command line arguments and call other modules to build study
    Structure outline
        1. command line argument parser
        2. validate file input/output names
        3. pass input file names to errors.py for future potential error handling
        4. parse the language input to define lexicon and grammar
        5. parse the study input to define experiment and create FindingFive objects
        6. write out the FindingFive objects (stimuli, responses, etc.) to output files
"""





## REQUIRED MODULES
import argparse
from backstage import errors, fileChecker
from backstage import stimuli, responses, trialTemplates, procedure, praat
from backstage import studyParser, languageParser,blockParser
import os

current_dir = os.getcwd()

# 1. Define a command-line parser object using argparse
parser = argparse.ArgumentParser(add_help = False,
                                 description = 'FindingFive Experiment Builder: builds the four components of a FindingFive ALL study out of 2 input files.')
inputs = parser.add_argument_group(title = 'input files (required)')
inputs.add_argument('study_input', metavar = '<study input csv>',
                    help = 'The name of a CSV file defining the study input')
inputs.add_argument('language_input', metavar = '<language input csv>',
                    help = 'The name of a CSV file defining the language input')
outputs = parser.add_argument_group(title = 'output files (optional)')
outputs.add_argument('-s', '--stimuli', metavar = '<stimuli output csv>', default = 'stimuli.csv',
                    help = 'The name of the CSV file defining the FindingFive stimuli. Default: "stimuli.csv"')
outputs.add_argument('-r', '--responses', metavar = '<responses output csv>', default = 'responses.csv',
                    help = 'The name of the CSV file defining the FindingFive responses. Default: "responses.csv"')
outputs.add_argument('-t', '--trials', metavar = '<trial templates output txt>', default = 'trial_templates.txt',
                    help = 'The name of the TXT file defining the FindingFive trial templates. Default: "trial_templates.txt"')
outputs.add_argument('-p', '--procedure', metavar = '<procedure output txt>', default = 'procedure.txt',
                    help = 'The name of the TXT file defining the FindingFive procedure. Default: "procedure.txt"')
outputs.add_argument('--praat', metavar = '<praat output txt>', default = 'praat.txt',
                    help = 'The name of the TXT file defining the sound files for Praat to concatenate. Default: "praat.txt"')
optional = parser.add_argument_group('additional optional arguments')
optional.add_argument('-h', '--help', action = 'help',
                      help = 'show this help message and exit')
optional.add_argument('-d', '--directory', metavar = '<directory>', default = current_dir,
                      help = 'The name of a directory in which to find the input files and save the output files (path must be relative to the current directory). Default: current working directory')
optional.add_argument('-o', '--overwrite', action = 'store_true',
                      help = 'Including this flag automatically writes over existing files with the same name as an output file. Excluding it prompts the user first')


args = parser.parse_args()

# 2. Fetch file names from the command line and validate them
study_input_file, language_input_file, stimuli_file, responses_file, trials_file, procedure_file, praat_file = fileChecker.main(args)

# 3. Pass input file names to errors.py for any error reporting
errors.study_input_file = study_input_file
errors.language_input_file = language_input_file

# 4. Call the language parser, set language info (see backstage/languageParser.py)
#details, grammar, lexicon = languageParser.main(language_input_file)
# details = session number, list number, grammar number
studyInfo = studyParser.readStduy('study_design_test.csv')
language = languageParser.main('input_language_test.csv')
blockParser.blockProcessor(studyInfo)

# 6. Write the outputs
stimuli.output(stimuli_file)
responses.output(responses_file)
trialTemplates.output(trials_file)
procedure.output(procedure_file)
praat.output(praat_file)

exit()
