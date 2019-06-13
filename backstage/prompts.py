#!/usr/bin/env python3

### prompts.py
# author: Noah R Nelson
# created: July 2018
# last modified by: Noah
# last modified on: 2018-08-04

import os

class Warning(object):
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        if self.msg is None:
            raise Exception('Warning! Something is not quite right. Exiting script.')

    def __str__(self):
        return self.msg


class FileExists(Warning):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'Warning! File "{file_name}" already exists! Input a new file name (or press <ENTER> to overwrite file):'.format(**kwargs)
        super().__init__(msg)
