#! /usr/bin/env python3

### errors.py
## Handle error reporting to the user

# input files (updated after import in studyParser and languageParser)
study_input_file = ''
language_input_file = ''

class PythonVersionError(Exception):
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        if self.msg is None:
            self.msg = 'Please run the code using Python version 3 (try using "python3" from command line). If you do not have python3 installed, you may need to install it.'

    def __str__(self):
        return self.msg


class InputError(Exception):
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        if self.msg is None:
            self.msg = 'Sorry! An unexpected error occurred while parsing the input files.'

    def __str__(self):
        return self.msg


class TextWithMicError(InputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'Please specify _either_ "Text" or "Mic_Check" in the input "{0}"'.format(study_input_file)
        super().__init__(msg)


class InputCompatibilityError(InputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'In the definition of the study details, the "{detail}" does not match across the study input file "{0}" and the language input file "{1}".'.format(study_input_file, language_input_file, **kwargs)
        super().__init__(msg)


class LanguageInputError(InputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'There was an unexpected error with the language input: "{0}"'.format(language_input_file)
        super().__init__(msg)

class UndefinedWordError(LanguageInputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'Undefined word(s) in phrase "{complex_noun}" (input: "{0}", row: {line_number}). Update lexicons in "{1}"?'.format(study_input_file, language_input_file, **kwargs)
        super().__init__(msg)

class LexiconDefinitionError(LanguageInputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'There is no lexical dictionary for category "{phrase_argument}" in "{1}" (input: "{0}", row: {line_number}).'.format(study_input_file, language_input_file, **kwargs)
        super().__init__(msg)


class StudyInputError(InputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'There was an unexpected error with the study input "{0}" at row {line_number}'.format(study_input_file, **kwargs)
        super().__init__(msg)

class PhraseParsingError(StudyInputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'Phrase parsing failed in phrase "{complex_noun}" (input: "{0}", row: {line_number})'.format(study_input_file, **kwargs)
        super().__init__(msg)

class RowParsingError(StudyInputError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'File line parsing error: (input: "{0}", row: {line_number}). Missing or invalid column value?'.format(study_input_file, **kwargs)
        super().__init__(msg)

class CellContentError(RowParsingError):
    def __init__(self, msg='', **kwargs):
        msg = '"{cell_content}" is not a recognized entry for "{linguistic_unit}" type block (input: "{0}", row: {line_number})'.format(study_input_file, **kwargs) + msg
        super().__init__(msg)

class FoilSpecificationError(RowParsingError):
    def __init__(self, msg='', **kwargs):
        msg = msg + '(input: "{0}", row: {line_number})'.format(study_input_file, **kwargs)
        super().__init__(msg)

class MissingArgumentError(RowParsingError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'Missing definition for "{phrase_argument}" (input: "{0}", row: {line_number})'.format(study_input_file, **kwargs)
        super().__init__(msg)

class ArgumentValueError(RowParsingError):
    def __init__(self, msg=None, **kwargs):
        msg = msg or 'The value of "{phrase_argument}" was not recognized (input: "{0}", row: {line_number}). Update lexicon in "{1}"?'.format(study_input_file, language_input_file, **kwargs)
        super().__init__(msg)
