#!/usr/bin/env python3

### praat.py
# author: Noah R Nelson
# created: July 2018
# last modified by: Noah
# last modified on: 2018-11-06

praat_content = []

def output(file):

	with open(file,"w") as f:
		for ls in praat_content:
			if len(ls) == 2:
				ls.append('\n')
			elif len(ls) != 3:
				raise ValueError('The constituent length is not correct. It should be either 2 (intransitive sentence) or 3 (transitive sentence)')
			else:
				pass
			for const in ls:
				f.write(const)
				f.write('\n')
