#! /usr/bin/env python3

### FindingFiveObjectClasses.py

## author: Noah R Nelson
## created: April 2017

## last modified by: Noah
## last modified on: 2018-11-05

# This module contains custom object classes defining FindingFive objects.


class Procedure(object):
    """
    Procedure objects are the FindingFive procedures,
    each for a given session (day) in the study
    """

    @property
    def number(self):
        return self._number
    @number.setter
    def number(self, value):
        if not isinstance (value, int):
            raise ValueError('The session number must be an integer')
        elif value <= 0 or value >= 5:
            raise ValueError('The session number must fall between 1 and 4')
        self._number = value

    # Procedure.blocks is an ordered list corresponding to the procedure:
    #+ what are the blocks ("blocks": {...}) AND what is the sequence
    @property
    def blocks(self):
        return self._blocks
    @blocks.setter
    def blocks(self, value):
        if not isinstance(value, list):
            raise TypeError('Blocks must be entered in an ordered list')
        if len(value) == 0:
            raise ValueError('You must define at least one block in a list')
        self._blocks = value


class FFobject(object):
    """
    This superclass defines FindingFive 'objects'.
    An FFobject is anything that must have a name in FindingFive
    """

    # FFobject.name defines the name that this object will have in FF
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('{} name must be entered as a string'.format(self))
        self._name = value


#_ This class is a subclass of FFobject that defines blocks

class Block(FFobject):
    """
    Block is a subclass of FFobject that defines FindingFive blocks.
    """

    @property
    def cover_trials(self):
        return self._cover_trials
    @cover_trials.setter
    def cover_trials(self, value):
        if not isinstance(value, list):
            raise TypeError('Cover_trials must be entered in an ordered list')
        self._cover_trials = value

    @property
    def end_trials(self):
        return self._end_trials
    @end_trials.setter
    def end_trials(self, value):
        if not isinstance(value, list):
            raise TypeError('End_trials must be entered in an ordered list')
        self._end_trials = value

    @property
    def templates(self):
        return self._templates
    @templates.setter
    def templates(self, value):
        if not isinstance(value, list):
            raise TypeError('Templates must be entered in a list')
        if len(value) == 0:
            raise ValueError('You must define at least one template in a list')
        self._templates = value

    @property
    def order(self):
        return self._order
    @order.setter
    def order(self, value):
        if value == "fixed" or value == "random" or value == "alternate":
            self._order = value
        else:
            raise ValueError('The trial_template presentation order must be "fixed", "random", or "alternate"')

    @property
    def repeat(self):
        return self._repeat
    @repeat.setter
    def repeat(self, value):
        if not isinstance(value, int):
            raise TypeError('Pattern repeat must be entered as an integer')
        self._repeat = value


class Template(FFobject):
    """
    Template is a subclass of FFobject that defines trial_templates.
    This class is primarily used for inheritance.
    To define templates, use subclasses for
    instruction (InstrTemplate), exposure (ExpTemplate), comprehension (CompTemplate),
    production (ProdTemplate), alternating trials (AltTemplate), or feedback (FeedBackTemplate).
    """

    def __init__(self):
        self._vertical_center = False
        self._force_response_delay = 'passive'

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if value in ['AFC', 'basic', 'instruction']:
            self._type = value
        else:
            raise TypeError('Trial templates must be of type "basic", "AFC", or "instruction"')

    @property
    def stimuli(self):
        return self._stimuli
    @stimuli.setter
    def stimuli(self, value):
        if not isinstance(value, list):
            raise TypeError('The stimuli must be entered in a list (empty list OK)')
        self._stimuli = value

    @property
    def vertical_center(self):
        return self._vertical_center
    @vertical_center.setter
    def vertical_center(self, value):
        if isinstance(value, bool):
            self._vertical_center = value
        else:
            raise TypeError('You must enter a boolean value for "vertical_center" (True or False)')

    @property
    def force_response_delay(self):
        return self._force_response_delay
    @force_response_delay.setter
    def force_response_delay(self, value):
        if value in ['active', 'passive', 'none']:
            self._force_response_delay = value
        else:
            raise TypeError('"force_response_delay" must be either "active", "passive", or "none"')

class InstrTemplate(Template):
    """
    InstrTemplate is a subclass of Template used for instruction templates.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'instruction'
### The following create duration and countdown_visible parameters
###+ duration delays the appearance of the 'Continue' button
###+ countdown_visible determines whether a countdown to the appearance of the button should be displayed
#        self._duration = 0
#        self._countdown_visible = False

#    @property
#    def duration(self):
#        return self._duration
#    @duration.setter
#    def duration(self, value):
#        if not isinstance(value, int) and not isinstance(value, float):
#            raise TypeError('Duration must be entered as a numeral (decimals OK)')
#        self._duration = value

#    @property
#    def countdown_visible(self):
#        return self._countdown_visible
#    @countdown_visible.setter
#    def countdown_visible(self, value):
#        if not isinstance(value, bool):
#            raise TypeError('You must enter a boolean value for "countdown_visible" (True or False)')
#        self._countdown_visible = value

class TextRespTemplate(Template):
    """
    TextRespTemplate is a subclass of Template used for free response textboxes.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'basic'

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        if not isinstance(value, list):
            raise TypeError('The responses must be entered in a list (empty list OK)')
        self._responses = value

class ExpTemplate(Template):
    """
    ExpTemplate is a subclass of Template used for exposure trials.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'basic'
        self._order = 'random'
        self._delay = 0.5
        self._replayable = True
        self._auto_advance = False

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        if not isinstance(value, list):
            raise TypeError('The responses must be entered in a list (empty list OK)')
        self._responses = value

    @property
    def order(self):
        return self._order
    @order.setter
    def order(self, value):
        if value == "alternate":
            raise ValueError('For alternate orders, use the AltTemplate subclass')
        if value == "fixed" or value == "random":
            self._order = value
        else:
            raise ValueError('The stimulus presentation order must be "fixed" or "random"')

    @property
    def delay(self):
        return self._delay
    @delay.setter
    def delay(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Delay must be entered as a numeral (0.5 recommended in most cases)')
        self._delay = value

#    @property
#    def duration(self):
#        return self._duration
#    @duration.setter
#    def duration(self, value):
#        if not isinstance(value, int) and not isinstance(value, float):
#            raise TypeError('Duration must be entered as a numeral (decimals OK)')
#        self._duration = value

    @property
    def replayable(self):
        return self._replayable
    @replayable.setter
    def replayable(self, value):
        if isinstance(value, bool):
            self._replayable = value
        else:
            raise TypeError('Replay setting must be entered as a boolean (True or False)')

    @property
    def auto_advance(self):
        return self._auto_advance
    @auto_advance.setter
    def auto_advance(self, value):
        if isinstance(value, bool):
            self._auto_advance = value
        else:
            raise TypeError('Auto_advance setting must be entered as a boolean (True or False)')

class CompTemplate(Template):
    """
    CompTemplate is a subclass of Template used for comprehension trials.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'AFC'
        self._order = 'random'
        self._delay = 0.5
        self._replayable = True

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        if not isinstance(value, list):
            raise TypeError('The responses must be entered in a list (empty list OK)')
        self._responses = value

    @property
    def order(self):
        return self._order
    @order.setter
    def order(self, value):
        if value == "alternate":
            raise ValueError('For alternate orders, use the AltTemplate subclass')
        if value == "fixed" or value == "random":
            self._order = value
        else:
            raise ValueError('The stimulus presentation order must be "fixed" or "random"')

    @property
    def delay(self):
        return self._delay
    @delay.setter
    def delay(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Delay must be entered as a numeral (0.3 recommended in most cases)')
        self._delay = value

    @property
    def replayable(self):
        return self._replayable
    @replayable.setter
    def replayable(self, value):
        if isinstance(value, bool):
            self._replayable = value
        else:
            raise TypeError('Replay setting must be entered as a boolean (True or False)')

class ProdTemplate(Template):
    """
    ProdTemplate is a subclass of Template used for production trials.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'basic'
        self._delay = 0.5
        self._replayable = False

    @property
    def responses(self):
        return self._responses
    @responses.setter
    def responses(self, value):
        if not isinstance(value, list):
            raise TypeError('The responses must be entered in a list (empty list OK)')
        self._responses = value

    @property
    def order(self):
        return self._order
    @order.setter
    def order(self, value):
        if value == "alternate":
            raise ValueError('For alternate orders, use the AltTemplate subclass')
        if value == "fixed" or value == "random":
            self._order = value
        else:
            raise ValueError('The stimulus presentation order must be "fixed" or "random"')

    @property
    def delay(self):
        return self._delay
    @delay.setter
    def delay(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Delay must be entered as a numeral (0.3 recommended in most cases)')
        self._delay = value

    @property
    def replayable(self):
        return self._replayable
    @replayable.setter
    def replayable(self, value):
        if isinstance(value, bool):
            self._replayable = value
        else:
            raise TypeError('Replay setting must be entered as a boolean (True or False)')

class AltTemplate(Template):
    """
    AltTemplate is a subclass of Template used for templates with alternating order.
    The alternation must be defined by some attribute
    """

    def __init__(self):
        Template.__init__(self)
        self.order = "alternate"

    @property
    def attribute(self):
        return self._attribute
    @attribute.setter
    def attribute(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute to alternate by must be entered as a string')
        self._attribute = value

class FeedBackTemplate(Template):
    """
    FeedBackTemplate is a subclass of Template used for
    custom feedback on noun production trials.
    """

    def __init__(self):
        Template.__init__(self)
        self.type = 'basic'
        self.order = 'fixed'
#        self._duration = 4

#    @property
#    def duration(self):
#        return self._duration
#    @duration.setter
#    def duration(self, value):
#        if not isinstance(value, int) and not isinstance(value, float):
#            raise TypeError('Duration must be entered as a numeral (decimals OK)')
#        self._duration = value

class Stimulus(FFobject):
    """
    Stimulus is a subclass of FFobject that defines stimuli.
    This class is only used for inheritance.
    To define stimuli, use subclasses for
    images (ImgStim), audio (AudStim), video (VidStim), or text (TextStim).
    """

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if not isinstance(value, str):
            raise TypeError('Stimulus type must be entered as a string')
        self._type = value

    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError('Stimulus content must be entered as a string')
        self._content = value


    # make the change here completely screw up things

    @property
    def barrier(self):
        return self._barrier
    @barrier.setter

    def barrier(self, value): # change the visible to barrier
        if isinstance (value, bool):
            self._barrier = value
        else:
            raise TypeError('Stimulus barrier must be entered as a boolean (True or False)')
    
    @property
    def visible(self):
        return self._visibles
    @visible.setter
    def visible(self, value):
        if not isinstance(value, bool):
            raise TypeError('Stimulus type must be entered as a string')
        self._visible = value

class ImgStim(Stimulus):
    """
    ImgStim is a subclass of Stimulus that defines image stimuli.
    Most image stimuli will need a defined width.
    """

    def __init__(self):
        Stimulus.__init__(self)
        self.type = 'image'
        #self._width = '200px'
        self.width = '200px'

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if not isinstance(value, str):
            raise TypeError('Stimulus width must be entered as a string')
        self._width = value

class AudStim(Stimulus):
    """
    AudStim is a subclass of Stimulus that defines audio stimuli.
    Audio stimuli should be invisible.
    """

    def __init__(self):
        Stimulus.__init__(self)
        self.type = 'audio'
        self._visible = False
        self._barrier = False

    @property
    def visible(self):
        return self._visible
    @visible.setter
    def visible(self, value):
        if not isinstance(value, str):
            raise TypeError('Stimulus visibility must be entered as a string')
        self._visible = value

class VidStim(Stimulus):
    """
    VidStim is a subclass of Stimulus that defines video stimuli.
    """

    def __init__(self):
        Stimulus.__init__(self)
        self.type = 'video'
        #self._width = '200px'
        self.width = '400px'
        self._visible = True
        self._barrier = False # zyy

class TextStim(Stimulus):
    """
    TextStim is a subclass of Stimulus that defines text stimuli.
    """

    def __init__(self):
        Stimulus.__init__(self)
        self.type = 'text'

    @property
    def alignment(self):
        return self._alignment
    @alignment.setter
    def alignment(self, value):
        if value == 'center' or value == 'left' or value == 'right':
            self._alignment = value
        else:
            raise TypeError('Text stimulus alignment must be "left", "right", or "center".')

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if isinstance(value, str):
            self._color = value
        else:
            raise TypeError('Please enter the text color as a string.')

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        if isinstance(value, str):
            self._size = value
        else:
            raise TypeError('Please enter the text size as a string.')

class Response(FFobject):
    """
    Response is a subclass of FFobject that defines responses.
    """

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if not isinstance(value, str):
            raise TypeError('Response type must be entered as a string')
        self._type = value

    @property
    def feedback(self):
        return self._feedback
    @feedback.setter
    def feedback(self, value):
        if not isinstance(value, bool):
            raise TypeError('Response feedback must be entered as a boolean (True or False)')
        self._feedback = value

    @property
    def instruction(self):
        return self._instruction
    @instruction.setter
    def instruction(self, value):
        if not isinstance(value, str):
            raise TypeError('Response instructions must be entered as a string')
        self._instruction = value


class ChoiceResponse(Response):
    """
    ChoiceResponse is a subclass of Response that defines choice responses (for AFC trials).
    """

    def __init__(self):
        Response.__init__(self)
        self.type = 'choice'
        self.feedback = True
        self._locations = 'random'

    @property
    def choices(self):
        return self._choices
    @choices.setter
    def choices(self, value):
        if not isinstance(value, list):
            raise TypeError('Response choices must be entered in a list')
        for choice in value:
            if not isinstance(choice, str):
                raise TypeError('Each choice in your list must be entered as a string')
        self._choices = value

    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, value):
        if not isinstance(value, str):
            raise TypeError('Response target must be entered as a string')
        self._target = value

    @property
    def sample_k(self):
        return self._sample_k
    @sample_k.setter
    def sample_k(self, value):
        if not isinstance(value, int):
            raise TypeError('The value of sample_k must be an integer')
        self._sample_k = value

    @property
    def locations(self):
        return self._locations
    @locations.setter
    def locations(self, value):
        if not isinstance(value, str):
            raise TypeError('Response locations must be entered as a string')
        if value == 'fixed' or value == 'random':
            self._locations = value
        else:
            raise ValueError('Response locations must be "fixed" or "random"')


class AudResponse(Response):
    """
    AudResponse is a subclass of Response that defines voice recording responses.
    """

    def __init__(self):
        Response.__init__(self)
        self.type = 'audio'
        self._location = 6

    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, value):
        if not isinstance(value, int):
            raise TypeError('Voice response location must be entered as an integer')
        if value < 1 or value > 9:
            raise ValueError('Voice response location must correspond to a slot in the 3x3 FindingFive grid')
        self._location = value


class TextResponse(Response):
    """
    TextResponse is a subclass of Response that defines free-response textbox responses.
    """

    def __init__(self):
        Response.__init__(self)
        self.type = 'text'
        self._max_char = 500
        self._required = True
        self.width = "700px" # marked by zyy, could be more custormized 
        self.height = "50px"

    @property
    def max_char(self):
        return self._max_char
    @max_char.setter
    def max_char(self, value):
        if not isinstance(value, int):
            raise TypeError('Maximum number of characters for free responses must be entered as an integer')
        if value < 100:
            raise ValueError('Be fair! Please allow responses of at least 100 characters')
        self._max_char = value

    @property
    def required(self):
        return self._required
    @required.setter
    def required(self, value):
        if isinstance(value, bool):
            self._required = value
        else:
            raise TypeError('Please enter the parameter "required" as a boolean (True or False).')
