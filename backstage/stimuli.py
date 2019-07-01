#!/usr/bin/env python3

### stimuli.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Noah
# last modified on: 2018-11-06

""" Create and build stimulus objects for a FindingFive study """

stimulus_objects = {}   # stimulus objects (used to populate stimuli_file)

from backstage import FindingFiveObjectClasses as FF, reformat

def text(name, content, **kwargs):
    text = FF.TextStim()
    text.name = name +'_text'
    text.content = content
    text.alignment = 'center'
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(text, key, value)
    stimulus_objects[text.name] = text

    return text.name

def audio(name, needs_text, **kwargs):
    aud = FF.AudStim()
    aud.name = name  + '_aud'
    aud.content = name + '.mp3'
    aud.barrier = False
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(aud, key, value)

    # If this study requires text version of audio stims...
    if needs_text == True:
        txt = FF.TextStim()
        txt.name = name + '_text'
        #txt.content = name.replace('_',' ')
        txt.content = name.replace('_',' ')
        txt.size = '2em'
        txt.alignment = 'center'
        # rename the audio stim for clarity
    #    aud.name = name + '_aud'
        # assign any kwargs (special params that deviate from the norm)
        for key, value in kwargs.items():
            setattr(txt, key, value)
        stimulus_objects[name] = txt

    stimulus_objects[aud.name] = aud
    return aud.name

def image(name, **kwargs):
    img = FF.ImgStim()
    img.name = name + '_img'
    img.content = name.replace('_img','') + '.png'
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(img, key, value)

    stimulus_objects[img.name] = img
    return img.name

def video(target, **kwargs):
    vid = FF.VidStim()
    vid.name = target + '_vid'
    vid.content = target + '.mp4'
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(vid, key, value)

    stimulus_objects[vid.name] = vid
    return vid.name

def feedback(name, needs_text, **kwargs):
    f = FF.AudStim()
    # audio stim name already updated with '_aud' if text-based study
    # remove it for now for consistency (gets returned later)
    name = name.replace('_aud','')
    f.name = name + '_feedback'
    f.content = name + '.mp3'
    f.delay = 2
    # assign any kwargs (special params that deviate from the norm)
    for key, value in kwargs.items():
        setattr(f, key, value)

    # are text forms required?
    if needs_text == True:
        t = FF.TextStim()
        t.name = name + '_feedback_text'
        # use spaces to separate words
        t.content = name.replace('_',' ')
        t.size = '2em'
        t.alignment = 'center'
        t.delay = 2
        # rename audio stim for clarity
        f.name = name + '_feedback_aud'
        # assign any kwargs (special params that deviate from the norm)
        for key, value in kwargs.items():
            setattr(t, key, value)
        stimulus_objects[t.name] = t

    stimulus_objects[f.name] = f
    return f.name


def Alienlumi():
    a = FF.ImgStim()
    a.name = 'Alien'
    a.content = 'alien_new.png'
    a.width = '70%'
    stimulus_objects[a.name] = a


def lumi():
    a = FF.ImgStim()
    a.name = 'Alien'
    a.content = 'alien_new.png'
    a.width = '70%'
    stimulus_objects[a.name] = a

    fb = FF.TextStim()
    fb.name = 'Lumi_says'
    fb.content = '<b>Now listen to how Lumi would say it</b>'
    fb.size = '1.25em'
    fb.alignment = 'center'
    fb.delay = 0.7
    stimulus_objects[fb.name] = fb

    e = FF.ImgStim()
    e.name = 'empty'
    e.content = 'whitespace.png'
    e.width = '5%'
    stimulus_objects[e.name] = e

    return [a.name, fb.name, e.name]

def output(stimuli_file,stimuli_identifiers):
    # get set of attributes across all stimuli
    stim_headers = set()
    for n, o in stimulus_objects.items(): # n = keys (names), o = values (objects)
        #print("before:",o.content)
        soundid, imageid, videoid = stimuli_identifiers
        if soundid:
            if '.mp3' in o.content:
                o.content = o.content.replace('.mp3',soundid+'.mp3')
        if imageid:
            if '.png' in o.content:
                o.content = o.content.replace('.png',soundid+'.png')
        if videoid:
            if '.mp4' in o.content:
                o.content = o.content.replace('.mp4',soundid+'.mp4')
        #print("after:",o.content)
        #print('\n')
                                       
        for attr in dir(o): # dir(o) gets a list of all attributes for object 'o'
            if attr.startswith('_'): # lots of Python inherent attributes, all have leading '_' or '__'
                continue
            else:
                stim_headers.add(attr)
    stim_headers = list(stim_headers)
    stim_headers_formatted = reformat.jsonStr(stim_headers).replace('[', '').replace(']', '').replace(', ', ',')

    # set values for each attribute for each stimulus and push into a master list
    FindingFiveStims = []
    for name, stimulus in stimulus_objects.items():
        attrs = []
        for attr in stim_headers: # should be ORDERED set, so no issues with ordering
            try:
                getattr(stimulus, attr)
            except AttributeError: # if the attribute belongs to a different object class
                attrs.append('') # it will have to be an empty cell in the csv
            else:
                attrs.append( getattr(stimulus, attr) )
        FindingFiveStims.append(attrs)

    csv_stims = reformat.jsonStr(FindingFiveStims)
    csv_stims_formatted = reformat.csvStr(csv_stims).replace("", '')

    # Now write that file!
    with open(stimuli_file, 'w') as outputTXT:
        outputTXT.write(stim_headers_formatted)
        outputTXT.write('\n')
        outputTXT.write(csv_stims_formatted)
