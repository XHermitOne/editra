###############################################################################
# Name: cobra.py                                                              #
# Purpose: Define Cobra syntax for highlighting and other features            #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Define support for Cobra programming language. 
@summary: Lexer configuration module for Cobra.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: _cobra.py 68798 2011-08-20 17:17:05Z CJP $"
__revision__ = "$Revision: 68798 $"

#-----------------------------------------------------------------------------#
# Imports
import wx.stc as stc

# Local Imports
from . import synglob
from . import syndata

#-----------------------------------------------------------------------------#

# Indenter keywords
INDENT_KW = ("body", "branch", "class", "cue", "def", "else", "except", 
             "expect", "finally", "for", "if", "invariant", "namespace",
             "on" "post", "shared", "success", "test", "try", "while")

UNINDENT_KW = ("return", "raise", "break", "continue", "pass")

# Cobra Keywords
KEYWORDS = ("abstract adds all and any as assert base be body bool branch "
            "break callable catch char class const continue cue decimal def do"
            "dynamic each else end ensure enum event every except expect "
            "extend extern fake false finally float for from get has if ignore "
            "implements implies import in inherits inlined inout int interface "
            "internal invariant is listen mixin must namespace new nil "
            "nonvirtual not number objc of off old on or out override partial "
            "pass passthrough post print private pro protected public raise "
            "ref require return same set shared sig stop struct success test "
            "this throw to to\\? trace true try uint use using var vari "
            "virtual where while yield")
KEYWORDS = (0, KEYWORDS)

#---- Syntax Style Specs ----#
SYNTAX_ITEMS = [ (stc.STC_P_DEFAULT, 'default_style'),
                 (stc.STC_P_CHARACTER, 'char_style'),
                 (stc.STC_P_CLASSNAME, 'class_style'),
                 (stc.STC_P_COMMENTBLOCK, 'comment_style'),
                 (stc.STC_P_COMMENTLINE, 'comment_style'),
                 (stc.STC_P_DECORATOR, 'decor_style'),
                 (stc.STC_P_DEFNAME, 'keyword3_style'),
                 (stc.STC_P_IDENTIFIER, 'default_style'),
                 (stc.STC_P_NUMBER, 'number_style'),
                 (stc.STC_P_OPERATOR, 'operator_style'),
                 (stc.STC_P_STRING, 'string_style'),
                 (stc.STC_P_STRINGEOL, 'stringeol_style'),
                 (stc.STC_P_TRIPLE, 'string_style'),
                 (stc.STC_P_TRIPLEDOUBLE, 'string_style'),
                 (stc.STC_P_WORD, 'keyword_style'),
                 (stc.STC_P_WORD2, 'userkw_style')]

#---- Extra Properties ----#
FOLD = ("fold", "1")
TIMMY = ("tab.timmy.whinge.level", "1") # Mark Inconsistant indentation

#-----------------------------------------------------------------------------#

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Cobra""" 
    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)

        # Setup
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [KEYWORDS, ]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [FOLD, TIMMY]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return ['#', ]

#-----------------------------------------------------------------------------#

def AutoIndenter(estc, pos, ichar):
    """Auto indent cobra code.
    @param estc: EditraStyledTextCtrl
    @param pos: current carat position
    @param ichar: Indentation character

    """
    line = estc.GetCurrentLine()
    spos = estc.PositionFromLine(line)
    text = estc.GetTextRange(spos, pos)
    eolch = estc.GetEOLChar()
    inspace = text.isspace()

    # Cursor is in the indent area somewhere
    if inspace:
        estc.AddText(eolch + text)
        return

    # Check if the cursor is in column 0 and just return newline.
    if not len(text):
        estc.AddText(eolch)
        return

    indent = estc.GetLineIndentation(line)
    if ichar == "\t":
        tabw = estc.GetTabWidth()
    else:
        tabw = estc.GetIndent()

    i_space = indent / tabw
    end_spaces = ((indent - (tabw * i_space)) * " ")

    tokens = [_f for _f in text.strip().split() if _f]
    if tokens and not inspace:
        if tokens[-1].endswith(""):
            if tokens[0] in INDENT_KW:
                i_space += 1
            elif tokens[0] in UNINDENT_KW:
                i_space = max(i_space - 1, 0)
        elif tokens[-1].endswith("\\"):
            i_space += 1

    rval = eolch + (ichar * i_space) + end_spaces
    if inspace and ichar != "\t":
        rpos = indent - (pos - spos)
        if rpos < len(rval) and rpos > 0:
            rval = rval[:-rpos]
        elif rpos >= len(rval):
            rval = eolch

    # Put text in the buffer
    estc.AddText(rval)
