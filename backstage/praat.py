#!/usr/bin/env python3

### praat.py
# author: Noah R Nelson
# created: July 2018
# last modified by: Noah
# last modified on: 2018-11-06

praat_content = {}

def append_content(order_of_words):
    global praat_content
    # using string rep to create hash to remove redundant entries
    string = '_'.join(order_of_words)
    praat_content[string] = order_of_words


def output(file):
    with open(file, 'w') as f:
        for string, list in praat_content.items():
            for line in list:
                f.write(line)
                f.write('\n')
