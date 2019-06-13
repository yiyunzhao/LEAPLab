#!/usr/bin/env python3

### fileChecker.py
# author: Noah R Nelson
# created: July 2018
# last modified by: Noah
# last modified on: 2018-11-06

import os
from backstage import errors, prompts

# pass args to fileChecker.main() as parsed command-line arguments
def main(args):
    """ Reads parsed and packaged command line arguments and sets file names accordingly """

    inputs = [args.study_input, args.language_input]
    outputs = [args.stimuli, args.responses, args.trials, args.procedure, args.praat]

    # handle --directory (-d) flag
    my_directory_in = args.directoryin
    my_directory_out = args.directoryout
    if my_directory_in is not None:
        inputs = [os.path.join(my_directory_in, file) for file in inputs]
    if my_directory_out is None:
        my_directory_out = my_directory_in


    # handle --overwrite (-o) flag
    overwrite = args.overwrite
    outputs = check_file_names(my_directory_out, outputs, overwrite)

    my_files = inputs + outputs
    return my_files

# check the file names using fileChecker.py
def check_file_names(directory, files, ignore = False):
    my_files = []
    for file in files:
        file_name = check(directory, file, ignore)
        my_files.append(file_name)
    return my_files

def check(directory, file, ignore = False):
    """Check the directory and file name to avoid overwriting"""
    # check directory, create if doesn't exist
    try: os.makedirs(directory, exist_ok = True)
    except TypeError: raise errors.PythonVersionError()
    # check for the file, prompt user if already exists
    path = os.path.join(directory, file)
    if os.path.exists(path):
        if ignore == False:
            filename = input( str(prompts.FileExists(file_name = path)) )
            if filename == '':
                filename = file
            filename = directory + '/' + filename
        else: filename = path
    else: filename = path

    return filename
