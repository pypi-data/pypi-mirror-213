# Generated from Turtle.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,35,87,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,5,0,
        28,8,0,10,0,12,0,31,9,0,1,1,1,1,1,1,1,1,3,1,37,8,1,1,2,1,2,1,2,1,
        2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,3,
        6,58,8,6,1,7,1,7,1,8,1,8,1,8,1,8,3,8,66,8,8,1,9,1,9,3,9,70,8,9,1,
        10,1,10,1,11,1,11,3,11,76,8,11,1,12,1,12,5,12,80,8,12,10,12,12,12,
        83,9,12,1,12,1,12,1,12,0,0,13,0,2,4,6,8,10,12,14,16,18,20,22,24,
        0,2,1,0,16,18,1,0,12,13,84,0,29,1,0,0,0,2,36,1,0,0,0,4,38,1,0,0,
        0,6,43,1,0,0,0,8,47,1,0,0,0,10,50,1,0,0,0,12,57,1,0,0,0,14,59,1,
        0,0,0,16,61,1,0,0,0,18,69,1,0,0,0,20,71,1,0,0,0,22,75,1,0,0,0,24,
        77,1,0,0,0,26,28,3,2,1,0,27,26,1,0,0,0,28,31,1,0,0,0,29,27,1,0,0,
        0,29,30,1,0,0,0,30,1,1,0,0,0,31,29,1,0,0,0,32,37,3,4,2,0,33,37,3,
        6,3,0,34,37,3,10,5,0,35,37,3,8,4,0,36,32,1,0,0,0,36,33,1,0,0,0,36,
        34,1,0,0,0,36,35,1,0,0,0,37,3,1,0,0,0,38,39,5,1,0,0,39,40,5,12,0,
        0,40,41,5,11,0,0,41,42,5,2,0,0,42,5,1,0,0,0,43,44,5,3,0,0,44,45,
        5,11,0,0,45,46,5,2,0,0,46,7,1,0,0,0,47,48,5,4,0,0,48,49,5,11,0,0,
        49,9,1,0,0,0,50,51,5,5,0,0,51,52,5,12,0,0,52,53,5,11,0,0,53,11,1,
        0,0,0,54,58,3,16,8,0,55,58,3,14,7,0,56,58,5,9,0,0,57,54,1,0,0,0,
        57,55,1,0,0,0,57,56,1,0,0,0,58,13,1,0,0,0,59,60,7,0,0,0,60,15,1,
        0,0,0,61,65,5,10,0,0,62,66,5,15,0,0,63,64,5,6,0,0,64,66,3,18,9,0,
        65,62,1,0,0,0,65,63,1,0,0,0,65,66,1,0,0,0,66,17,1,0,0,0,67,70,5,
        11,0,0,68,70,3,20,10,0,69,67,1,0,0,0,69,68,1,0,0,0,70,19,1,0,0,0,
        71,72,7,1,0,0,72,21,1,0,0,0,73,76,5,14,0,0,74,76,3,24,12,0,75,73,
        1,0,0,0,75,74,1,0,0,0,76,23,1,0,0,0,77,81,5,7,0,0,78,80,5,26,0,0,
        79,78,1,0,0,0,80,83,1,0,0,0,81,79,1,0,0,0,81,82,1,0,0,0,82,84,1,
        0,0,0,83,81,1,0,0,0,84,85,5,8,0,0,85,25,1,0,0,0,7,29,36,57,65,69,
        75,81
    ]

class TurtleParser ( Parser ):

    grammarFileName = "Turtle.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'@prefix'", "'.'", "'@base'", "'BASE'", 
                     "'PREFIX'", "'^^'", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "BooleanLiteral", "String", "IRIREF", 
                      "PNAME_NS", "PNAME_LN", "BLANK_NODE_LABEL", "LANGTAG", 
                      "INTEGER", "DECIMAL", "DOUBLE", "EXPONENT", "STRING_LITERAL_QUOTE", 
                      "STRING_LITERAL_SINGLE_QUOTE", "STRING_LITERAL_LONG_SINGLE_QUOTE", 
                      "STRING_LITERAL_LONG_QUOTE", "UCHAR", "ECHAR", "WS", 
                      "PN_CHARS_BASE", "PN_CHARS_U", "PN_CHARS", "PN_PREFIX", 
                      "PN_LOCAL", "PLX", "PERCENT", "HEX", "PN_LOCAL_ESC" ]

    RULE_turtleDoc = 0
    RULE_directive = 1
    RULE_prefixID = 2
    RULE_base = 3
    RULE_sparqlBase = 4
    RULE_sparqlPrefix = 5
    RULE_literal = 6
    RULE_numericLiteral = 7
    RULE_rdfLiteral = 8
    RULE_iri = 9
    RULE_prefixedName = 10
    RULE_blankNode = 11
    RULE_anon = 12

    ruleNames =  [ "turtleDoc", "directive", "prefixID", "base", "sparqlBase", 
                   "sparqlPrefix", "literal", "numericLiteral", "rdfLiteral", 
                   "iri", "prefixedName", "blankNode", "anon" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    BooleanLiteral=9
    String=10
    IRIREF=11
    PNAME_NS=12
    PNAME_LN=13
    BLANK_NODE_LABEL=14
    LANGTAG=15
    INTEGER=16
    DECIMAL=17
    DOUBLE=18
    EXPONENT=19
    STRING_LITERAL_QUOTE=20
    STRING_LITERAL_SINGLE_QUOTE=21
    STRING_LITERAL_LONG_SINGLE_QUOTE=22
    STRING_LITERAL_LONG_QUOTE=23
    UCHAR=24
    ECHAR=25
    WS=26
    PN_CHARS_BASE=27
    PN_CHARS_U=28
    PN_CHARS=29
    PN_PREFIX=30
    PN_LOCAL=31
    PLX=32
    PERCENT=33
    HEX=34
    PN_LOCAL_ESC=35

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TurtleDocContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def directive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TurtleParser.DirectiveContext)
            else:
                return self.getTypedRuleContext(TurtleParser.DirectiveContext,i)


        def getRuleIndex(self):
            return TurtleParser.RULE_turtleDoc

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTurtleDoc" ):
                return visitor.visitTurtleDoc(self)
            else:
                return visitor.visitChildren(self)




    def turtleDoc(self):

        localctx = TurtleParser.TurtleDocContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_turtleDoc)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 58) != 0):
                self.state = 26
                self.directive()
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirectiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def prefixID(self):
            return self.getTypedRuleContext(TurtleParser.PrefixIDContext,0)


        def base(self):
            return self.getTypedRuleContext(TurtleParser.BaseContext,0)


        def sparqlPrefix(self):
            return self.getTypedRuleContext(TurtleParser.SparqlPrefixContext,0)


        def sparqlBase(self):
            return self.getTypedRuleContext(TurtleParser.SparqlBaseContext,0)


        def getRuleIndex(self):
            return TurtleParser.RULE_directive

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirective" ):
                return visitor.visitDirective(self)
            else:
                return visitor.visitChildren(self)




    def directive(self):

        localctx = TurtleParser.DirectiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_directive)
        try:
            self.state = 36
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 32
                self.prefixID()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 33
                self.base()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 34
                self.sparqlPrefix()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 35
                self.sparqlBase()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrefixIDContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PNAME_NS(self):
            return self.getToken(TurtleParser.PNAME_NS, 0)

        def IRIREF(self):
            return self.getToken(TurtleParser.IRIREF, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_prefixID

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixID" ):
                return visitor.visitPrefixID(self)
            else:
                return visitor.visitChildren(self)




    def prefixID(self):

        localctx = TurtleParser.PrefixIDContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_prefixID)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(TurtleParser.T__0)
            self.state = 39
            self.match(TurtleParser.PNAME_NS)
            self.state = 40
            self.match(TurtleParser.IRIREF)
            self.state = 41
            self.match(TurtleParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BaseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IRIREF(self):
            return self.getToken(TurtleParser.IRIREF, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_base

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase" ):
                return visitor.visitBase(self)
            else:
                return visitor.visitChildren(self)




    def base(self):

        localctx = TurtleParser.BaseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_base)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(TurtleParser.T__2)
            self.state = 44
            self.match(TurtleParser.IRIREF)
            self.state = 45
            self.match(TurtleParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SparqlBaseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IRIREF(self):
            return self.getToken(TurtleParser.IRIREF, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_sparqlBase

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSparqlBase" ):
                return visitor.visitSparqlBase(self)
            else:
                return visitor.visitChildren(self)




    def sparqlBase(self):

        localctx = TurtleParser.SparqlBaseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_sparqlBase)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(TurtleParser.T__3)
            self.state = 48
            self.match(TurtleParser.IRIREF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SparqlPrefixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PNAME_NS(self):
            return self.getToken(TurtleParser.PNAME_NS, 0)

        def IRIREF(self):
            return self.getToken(TurtleParser.IRIREF, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_sparqlPrefix

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSparqlPrefix" ):
                return visitor.visitSparqlPrefix(self)
            else:
                return visitor.visitChildren(self)




    def sparqlPrefix(self):

        localctx = TurtleParser.SparqlPrefixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_sparqlPrefix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(TurtleParser.T__4)
            self.state = 51
            self.match(TurtleParser.PNAME_NS)
            self.state = 52
            self.match(TurtleParser.IRIREF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rdfLiteral(self):
            return self.getTypedRuleContext(TurtleParser.RdfLiteralContext,0)


        def numericLiteral(self):
            return self.getTypedRuleContext(TurtleParser.NumericLiteralContext,0)


        def BooleanLiteral(self):
            return self.getToken(TurtleParser.BooleanLiteral, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_literal

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = TurtleParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_literal)
        try:
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10]:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.rdfLiteral()
                pass
            elif token in [16, 17, 18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.numericLiteral()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.match(TurtleParser.BooleanLiteral)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumericLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(TurtleParser.INTEGER, 0)

        def DECIMAL(self):
            return self.getToken(TurtleParser.DECIMAL, 0)

        def DOUBLE(self):
            return self.getToken(TurtleParser.DOUBLE, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_numericLiteral

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumericLiteral" ):
                return visitor.visitNumericLiteral(self)
            else:
                return visitor.visitChildren(self)




    def numericLiteral(self):

        localctx = TurtleParser.NumericLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_numericLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 458752) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RdfLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def String(self):
            return self.getToken(TurtleParser.String, 0)

        def LANGTAG(self):
            return self.getToken(TurtleParser.LANGTAG, 0)

        def iri(self):
            return self.getTypedRuleContext(TurtleParser.IriContext,0)


        def getRuleIndex(self):
            return TurtleParser.RULE_rdfLiteral

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRdfLiteral" ):
                return visitor.visitRdfLiteral(self)
            else:
                return visitor.visitChildren(self)




    def rdfLiteral(self):

        localctx = TurtleParser.RdfLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_rdfLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(TurtleParser.String)
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.state = 62
                self.match(TurtleParser.LANGTAG)
                pass
            elif token in [6]:
                self.state = 63
                self.match(TurtleParser.T__5)
                self.state = 64
                self.iri()
                pass
            elif token in [-1]:
                pass
            else:
                pass
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IriContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IRIREF(self):
            return self.getToken(TurtleParser.IRIREF, 0)

        def prefixedName(self):
            return self.getTypedRuleContext(TurtleParser.PrefixedNameContext,0)


        def getRuleIndex(self):
            return TurtleParser.RULE_iri

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIri" ):
                return visitor.visitIri(self)
            else:
                return visitor.visitChildren(self)




    def iri(self):

        localctx = TurtleParser.IriContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_iri)
        try:
            self.state = 69
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.match(TurtleParser.IRIREF)
                pass
            elif token in [12, 13]:
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.prefixedName()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrefixedNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PNAME_LN(self):
            return self.getToken(TurtleParser.PNAME_LN, 0)

        def PNAME_NS(self):
            return self.getToken(TurtleParser.PNAME_NS, 0)

        def getRuleIndex(self):
            return TurtleParser.RULE_prefixedName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixedName" ):
                return visitor.visitPrefixedName(self)
            else:
                return visitor.visitChildren(self)




    def prefixedName(self):

        localctx = TurtleParser.PrefixedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_prefixedName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            _la = self._input.LA(1)
            if not(_la==12 or _la==13):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlankNodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLANK_NODE_LABEL(self):
            return self.getToken(TurtleParser.BLANK_NODE_LABEL, 0)

        def anon(self):
            return self.getTypedRuleContext(TurtleParser.AnonContext,0)


        def getRuleIndex(self):
            return TurtleParser.RULE_blankNode

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlankNode" ):
                return visitor.visitBlankNode(self)
            else:
                return visitor.visitChildren(self)




    def blankNode(self):

        localctx = TurtleParser.BlankNodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_blankNode)
        try:
            self.state = 75
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.match(TurtleParser.BLANK_NODE_LABEL)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 74
                self.anon()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AnonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(TurtleParser.WS)
            else:
                return self.getToken(TurtleParser.WS, i)

        def getRuleIndex(self):
            return TurtleParser.RULE_anon

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnon" ):
                return visitor.visitAnon(self)
            else:
                return visitor.visitChildren(self)




    def anon(self):

        localctx = TurtleParser.AnonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_anon)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(TurtleParser.T__6)
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 78
                self.match(TurtleParser.WS)
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 84
            self.match(TurtleParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





