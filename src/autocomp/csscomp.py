###############################################################################
# Name: csscomp.py                                                            #
# Purpose: Simple input assistant for CSS                                     #
# Author: Cody Precord                                                        #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Simple autocompletion support for Cascading Style Sheets.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__cvsid__ = "$Id: csscomp.py 70229 2012-01-01 01:27:10Z CJP $"
__revision__ = "$Revision: 70229 $"

#--------------------------------------------------------------------------#
# Imports
import re
import wx
import wx.stc

# Local Imports
from . import completer

#--------------------------------------------------------------------------#

# Regular Expressions
RE_LINK_PSEUDO = re.compile("a:(link|visited|active|hover|focus)*")
RE_CSS_COMMENT = re.compile("\/\*[^*]*\*+([^/][^*]*\*+)*\/")
RE_CSS_BLOCK = re.compile("\{[^}]*\}")

PSUEDO_SYMBOLS = completer.CreateSymbols([ 'active', 'focus', 'hover', 
                                           'link', 'visited' ],
                                         )

#--------------------------------------------------------------------------#

class Completer(completer.BaseCompleter):
    """CSS Code completion provider"""
    def __init__(self, stc_buffer):
        super(Completer, self).__init__(stc_buffer)

        # Setup
        self.SetAutoCompKeys([ord(':'), ord('.') ])
        self.SetAutoCompStops(' {}#')
        self.SetAutoCompFillups('')
        self.SetCallTipKeys([ord('('), ])
        self.SetCallTipCancel([ord(')'), wx.WXK_RETURN])
        
    def GetAutoCompList(self, command):
        """Returns the list of possible completions for a command string.
        @param command: command lookup is done on

        """
        buff = self.GetBuffer()
        keywords = buff.GetKeywords()
        if command in [None, '']:
            return completer.CreateSymbols(keywords, completer.TYPE_UNKNOWN)

        cpos = buff.GetCurrentPos()
        cline = buff.GetCurrentLine()
        lstart = buff.PositionFromLine(cline)
        tmp = buff.GetTextRange(lstart, cpos).rstrip()

        # Check for the case of a pseudo class
        if IsPsuedoClass(command, tmp):
            return PSUEDO_SYMBOLS

        # Give some help on some common properties
        if tmp.endswith(':'):
            word = GetWordLeft(tmp.rstrip().rstrip(':'))
            comps = PROP_OPTS.get(word, list())
            comps = list(set(comps))
            comps.sort()
            return completer.CreateSymbols(comps, completer.TYPE_PROPERTY)

        # Look for if we are completing a tag class
        if tmp.endswith('.'):
            classes = list()
            if not buff.IsString(cpos):
                txt = buff.GetText()
                txt = RE_CSS_COMMENT.sub('', txt)
                txt = RE_CSS_BLOCK.sub(' ', txt)
                for token in txt.split():
                    if '.' in token:
                        classes.append(token.split('.', 1)[-1])

                classes = list(set(classes))
                classes.sort()
            return completer.CreateSymbols(classes, completer.TYPE_CLASS)

        return completer.CreateSymbols(keywords, completer.TYPE_UNKNOWN)

    def GetCallTip(self, command):
        """Returns the formated calltip string for the command."""
        if command == 'url':
            return 'url(\'../path\')'
        else:
            return ''

    def ShouldCheck(self, cpos):
        """Should completions be attempted
        @param cpos: current buffer position
        @return: bool

        """
        buff = self.GetBuffer()
        rval = True
        if buff is not None:
            if buff.IsComment(cpos):
                rval =  False
        return rval

#--------------------------------------------------------------------------#

def IsPsuedoClass(cmd, line):
    """Check the line to see if its a link pseudo class
    @param cmd: current command
    @param line: line of the command
    @return: bool

    """
    if cmd.endswith(':'):
        token = line.split()[-1]
        pieces = token.split(":")
        if pieces[0] == 'a' or pieces[0].startswith('a.'):
            return True
    return False

def GetWordLeft(line):
    """Get the first valid word to the left of the end of line
    @param line: Line text
    @return: string

    """
    for idx in range(1, len(line)+1):
        ch = line[idx*-1]
        if ch.isspace() or ch in '{;':
            return line[-1*idx:].strip()
    else:
        return ''

#--------------------------------------------------------------------------#

# Properties to provide some input help on
PROP_OPTS = { 'border-style' : ['none', 'hidden', 'dotted', 'dashed',
                                 'solid', 'double', 'groove', 'ridge',
                                 'inset', 'outset'],
              'float' : ['left', 'right', 'none'],
              'font-style' : ['normal', 'italic', 'oblique'],
              'font-weight' : ['normal', 'bold', 'lighter', 'bolder'],
              'list-style-type' : ['none', 'disc', 'circle', 'square',
                                    'decimal', 'decimal-leading-zero',
                                    'lower-roman', 'upper-roman',
                                    'lower-alpha', 'upper-alpha',
                                    'lower-greek', 'lower-latin', 'hebrew',
                                    'armenian', 'georgian', 'cjk-ideographic',
                                    'hiragana', 'katakana',
                                    'hiragana-iroha', 'katakana-iroha'],
              'text-decoration' : ['none', 'underline', 'line-through',
                                    'overline', 'blink'],
              'text-align' : ['left', 'right', 'center', 'justify'],
              'vertical-align' : ['baseline', 'sub', 'super', 'top',
                                   'text-top', 'middle', 'bottom',
                                   'text-bottom', ]
              }

