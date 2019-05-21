#!/usr/bin/env python3

### reformat.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Noah
# last modified on: 2018-08-02

""" Reformat string representations of FindingFive objects for file outputs """

import json, os, ntpath, re

def jsonStr(content):
    return json.dumps(content)

def csvStr(dump):
    nest = 0 # how nested is the current string? (1 tab per level of nesting)
    quot = 0 # track whether inside our outside of quotes
    dump_formatted = ''
    for char in dump:
        if char == '[':
            nest += 1
            # skip the first two list bracket openers (meta list and row list)
            if nest == 1 or nest == 2: continue
            else: char = '"["'
        if char == ']':
            nest -= 1
            # skip the last two list bracket closers (meta list and row list)
            if nest == 0 or nest == 1: continue
            else: char = '"]"'
        # if we hit the end of a row
        if char == ',':
            if nest < 2: char = '\n'
            if nest > 2: char = '","'
        if char == ' ' and nest < 2: continue
        # track quotes
        if char == '"': quot += 1
        # spaces outside of quotes should be ignored
        if char == ' ' and quot % 2 == 0: continue
        dump_formatted += char

    return dump_formatted

def txtStr(dump):
    nest = 0 # how nested is the current string? (how much to indent)
    dump_formatted = ''
    for char in dump:
        if char == '{' or char == '[':
            nest += 1
            char = char + "\n" + "\t"*nest
        if char == '}' or char == ']':
            nest -= 1
            char = "\n" + "\t"*nest + char
        if char == ',':
            if nest == 1:
                char = char + "\n"*2 + "\t"
            else:
                char = char + "\n" + "\t"*nest
        dump_formatted += char

    return dump_formatted.replace(' ', '')

def ffStr(ff_str):
    ff_formatted = repr(ff_str).replace('\'', '"')
    ff_formatted = ff_formatted.replace('True', 'true')
    ff_formatted = ff_formatted.replace('False', 'false')
    return ff_formatted
