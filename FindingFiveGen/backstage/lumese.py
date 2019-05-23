#!/usr/bin/env python3

### lumese.py
# author: Noah R Nelson
# created: August 2018
# last modified by: Yiyun Zhao
# last modified on: 2019-Feb-26

""" Parse /*phrases*/ and translate to 'lumese' for audio files """
""" Phrases in StudyInput are encoded in this way: chefOnBlueSkateboard; chefOnTable; BlueTable; """

# search dictionary
# code marker: [!?Q] --> doubts  




## REQUIRED MODULES
import re, ntpath
from backstage import languageParser as LP, errors
# WHen we import languageParser, we can call a series of variables: 
# nouns, adjectives, verbs, adpositons, case_markers, word_orders, pp_types, pp_norm, LanguageInputDetails, LexiconTypeDic

# function for the lowercaseing of first letter only
lower_first_letter = lambda s: s[:1].lower() + s[1:] if s else ''
# function for the uppoercaseing of first letter only
upper_first_letter = lambda s: s[:1].upper() + s[1:] if s else ''



#***************Simple Words **********************************
def SimpleWord(content, lingUnit, input_line_number=None):
    if lingUnit == 'mix':
        vocabulary = LP.Info['lexicon']['master_lexicon'] # this attribute is inherited in the LanguageParser.py
    else:
        vocabulary = LP.Info['lexicon'][lingUnit.lower()]

    # translate this word in Lumi
    try:
        content_inLumi = vocabulary[content]
    
    except:
        raise Exception('Invalid input! ' + content + ' cannot be translated into '+ lingUnit + 'in Lumi')

    return content_inLumi



#*************** Complex Noun Phrases **********************************
def ParsePhrase(ComplexNoun, input_line_number=None):
    """Take a multi-word cell of the input file and parse it into components
        Support complexNouns: ['refOnRedSkateboard','refOnSkateboard','RedSkateboard','OnBlueSkateboard']

    Input: an complex Phrase as previously indicated
    Output: the translated version of the input [List]: [head_noun, adpos, adj, other_noun]

    """

    # split the multi-word noun by capital letters
    words = re.findall('[A-Z][^A-Z]+', upper_first_letter(ComplexNoun))
    # lowercase everybody for dictionary identification...
    for i in range( len(words) ):
        words[i] = words[i].lower()
    # some checks for whether parsing was successful
    if type(words) is not list:
        raise errors.PhraseParsingError(complex_noun = ComplexNoun, line_number = input_line_number)
    #elif len(words) == 1:
    if len(words) == 1:
        raise errors.PhraseParsingError(complex_noun = ComplexNoun, line_number = input_line_number)

    # initialize part of speech variables
    head_noun, adpos, adj, other_noun = None, None, None, None
    print(words)
    my_phrase = []
    ind = 0
    try:
        while ind<len(words):
            if LP.LexiconTypeDic[words[ind]] == 'nouns':
                if head_noun == None:
                    head_noun = LP.nouns[words[ind]]
                    ind += 1
                else:
                    pass
            else:
                head_noun = ''

            if ind >=len(words):break

            if LP.LexiconTypeDic[words[ind]] == 'adpositions':
                adpos = LP.adpositions[words[ind]]
                ind+=1
            else:
                adpos = ''

            if ind >=len(words):break

            if LP.LexiconTypeDic[words[ind]] == 'adjectives':
                adj = LP.adjectives[words[ind]]
                ind+=1
            else:
                adj = ''

            if ind >= len(words):break

            if LP.LexiconTypeDic[words[ind]] == 'nouns':
                other_noun = LP.nouns[words[ind]]
                ind+=1
            else:
                other_noun = ''

    except KeyError: # key error implies misparsed phrase
        raise errors.UndefinedWordError(complex_noun = ComplexNoun, line_number = input_line_number)

    # construct output
    my_phrase = [head_noun, adpos, adj, other_noun]
    return my_phrase

def ReorderPhrase(my_phrase, input_line_number=None, CaseMarker=None, PpType=None, PpNom=None):
    """Reorder parsed English phrase content into Lumese phrase order"""
    # NOTE: must ensure that this isn't called for sentence production blocks

    # the word order is determined by the two information:
    # PpType which determines the relationship between head noun and PP phrase
    # PpNom which determines the relationship between the adposition and modified noun
    '''
    example: chef under table [ENGLISH]
    Pptype == pre & PpNorm == pre: under table chef
    Pptype == pre & PpNorm == post: chef under table
    Pptype == post & PpNorm == pre: table under chef
    Pptype == post & PpNorm = post: chef table under

    Input: the phrase already translated in the Lumese: e.g. ['forpah', 'sool', 'redler', 'lanferda'] 
    Output: a tuple (the Reordered Phrase, its Corresponding Structure) e.g., ('forpah_sool_redler_lanferda', 'headNoun_adpos_adj_otherNoun')

    '''

    head_noun, adpos, adj, other_noun = my_phrase
    my_phrase_order = ''
    Lumese = ''


    # preposition phrase
    if head_noun == None and PpType == 'pre':
        Lumese = [adp, adj,other_noun]
        my_phrase_order = ['adp','adj','otherNoun']

    # post position phrase
    elif head_noun == None and PpType == 'post':
        Lumese = [adj, other_noun, adp]
        my_phrase_order = ['adj','otherNoun','adp']

    # adpos, adj, other_noun, head_noun phrase
    elif PpType == 'pre' and PpNom == 'pre':
        Lumese = [adpos, adj, other_noun, head_noun]
        my_phrase_order = ['adpos','adj','otherNoun','headNoun']

    elif PpType == 'pre' and PpNom == 'post':
        Lumese = [head_noun,adpos, adj, other_noun]
        my_phrase_order = ['headNoun','adpos','adj','otherNoun']

    elif PpType == 'post' and PpNom == 'pre':
        Lumese = [adj, other_noun, adpos, head_noun]
        my_phrase_order = ['adj', 'otherNoun', 'adpos', 'headNoun']

    elif PpType == 'post' and PpNom == 'post':
        Lumese = [head_noun, adj, other_noun, adpos]
        my_phrase_order = ['headNoun', 'adj', 'otherNoun', 'adpos']
    else:
        raise Exception("Please Specify the PpType and PpNom of your Complex Noun Phrase")

    # exclude unfilled position
    Lumese_final = []
    my_phrase_order_final = []
    for ind, word in enumerate(Lumese):
        if word:
            Lumese_final.append(word)
            my_phrase_order_final.append(my_phrase_order[ind])

    audio = '_'.join(Lumese_final)
    return (audio, '_'.join(my_phrase_order_final))


#def OrderComplexNoun(ComplexNoun, CaseMarker = None, PpType = None, PpNom = None, line_number = None):
def ComplexNoun(ComplexNoun, CaseMarker = None, PpType = None, PpNom = None, line_number = None):
    """Parse a phrase or complex noun into component words and rebuild into Lumese"""
    """ didn't pass the order information yet, probably for the future use (e.g.,case marking on complex Nouns)"""
    
    my_phrase = ParsePhrase(ComplexNoun, line_number)
    #print('my_phrase',my_phrase)
    audio, order = ReorderPhrase(my_phrase, line_number, CaseMarker, PpType, PpNom)
    #print(audio, order)
    return audio, order


#*************** Sentences **********************************

def CaseWord(word,CaseMarker,position):
    
    try:
        case = LP.Info['lexicon']['case_markers'][CaseMarker]
    except:
        raise Exception(CaseMarker+' does not exisit')

    if position.lower().startswith('pre'):
        casedword = case+word
    elif position.lower().startswith('suf'):
        casedword = word+case
    else:
        raise Exception('poistion is in valid, it could be either prefix or suffix.')

    return casedword

def CasePhrase(sequence,wordorder,target,CaseMarker,position):
    sequence_list = sequence.split('_')
    wordorder_list = wordorder.split('_')
    target_pos = wordorder_list.index(target)
    sequence_list[target_pos] = CaseWord(sequence_list[target_pos],CaseMarker,position)

    return '_'.join(sequence_list)


def ParseSentence(sentence,CaseMarker=None, position=None, PpType=None, PpNom=None, line_number=None):
    
    # check whether the subject or object involves adpositional phrase

    ####### Translatetion Part #######
    # 1. translate subject
    #print("Parse Sentence")
    Subject, Object, Verb = sentence[0:3]
    Subject_lumese, Subject_order, Object_lumese, Object_order, Verb_lumese = None,None,None,None,None

    if not Subject:
        pass
    elif Subject in LP.Info['lexicon']['nouns']:
        Subject_lumese,Subject_order = SimpleWord(Subject, 'nouns'),None
    else:
        try:
            Subject_lumese, Subject_order = ComplexNoun(Subject, PpType=PpType, PpNom=PpNom)
        except:
            raise Exception('Invalid Subject, either the word is not a noun or the complex noun formed incorrectly')

    #2. translate object
    if not Object:
        pass
    elif Object in LP.Info['lexicon']['nouns']:
        Object_lumese, Object_order = SimpleWord(Object, 'nouns'), None
    else:
        try:
            Object_lumese, Object_order = ComplexNoun(Object, PpType=PpType, PpNom=PpNom)
        except:
            raise Exception('Invalid Object, either the word is not a noun or the complex noun formed incorrectly')
    
    # 3. translate verb 
    try:
        Verb_lumese = SimpleWord(Verb,'verbs')
    except:
        raise Exception('Verb is missing in the sentence')




    ####### Adding the caseMarker #########
    if CaseMarker == 'NCM' or not CaseMarker:
        pass
    else:
        # mark the subject 
        if CaseMarker in ['SNOUN','CM','SVERB']:
            try:
                if Subject_order:
                    Subject_lumese = CasePhrase(Subject_lumese,Subject_order,'headNoun',CaseMarker,position)
                    #print("Subj",Subject_lumese)
                else:
                    Subject_lumese = CaseWord(Subject_lumese,CaseMarker,position)
                    #print("Subj",Subject_lumese)
            except:
                raise Exception("Cannot add the case to the subject")
        
        if CaseMarker in ['ONOUN', "CM","OVERB"]:
            try:
                if Object_order:
                    Object_lumese = CasePhrase(Object_lumese,Object_order,'headNoun',CaseMarker,position)
                    #print("Obj",Object_lumese)
                else:
                    Object_lumese = CaseWord(Object_lumese,CaseMarker,position)
                    #print("Obj",Object_lumese)
            except:
                raise Exception('Cannot add the case to the object')

        if CaseMarker in ['SVERB',"OVERB"]:
            try:
                Verb_lumese = CaseWord(Verb_lumese,CaseMarker,position)
                #print("Verb",Verb_lumese)
            except:
                raise Exception('Cannot add the case to the verb')

    return (Subject_lumese, Object_lumese, Verb_lumese)

def ReorderSentence(my_sentence, wordorder,line_number):
    sentDic = dict(zip('SOV',my_sentence))
    mysent = [sentDic[i] for i in wordorder.upper()]
    try:
        orderedSent = '_'.join(mysent)
    except:
        raise Exception("One of the element in sentence (Subject, Verb, Object) is invalid so it cannot be aggregated")
    return orderedSent, wordorder
    

def Sentence(sentence, wordorder, CaseMarker = None, position=None, PpType = None, PpNom = None, line_number = None):
    """Parse a phrase or sentences noun into component words and rebuild into Lumese"""
    """ didn't pass the order information yet, probably for the future use (e.g.,case marking on complex Nouns)"""
    
    my_sentence = ParseSentence(sentence, CaseMarker, position, PpType, PpNom,line_number)
    #print("mysent:",my_sentence)
    audio,order = ReorderSentence(my_sentence, wordorder,line_number)
    #print("audio:",audio)
    return audio, order






































