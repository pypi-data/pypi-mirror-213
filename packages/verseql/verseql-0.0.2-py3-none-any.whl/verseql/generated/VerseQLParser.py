# flake8: noqa
# type: ignore
# Generated from verseql/grammar/VerseQLParser.g4 by ANTLR 4.13.0
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
        4,1,53,237,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,1,0,1,0,1,0,1,0,1,0,1,0,3,0,41,8,0,
        1,1,1,1,1,1,3,1,46,8,1,1,1,3,1,49,8,1,1,1,3,1,52,8,1,1,1,3,1,55,
        8,1,1,2,1,2,1,2,1,2,3,2,61,8,2,1,3,1,3,1,3,5,3,66,8,3,10,3,12,3,
        69,9,3,1,4,1,4,1,4,3,4,74,8,4,1,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,94,8,7,1,7,1,7,1,7,1,7,
        1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,113,8,7,
        1,7,1,7,1,7,1,7,1,7,5,7,120,8,7,10,7,12,7,123,9,7,1,7,1,7,5,7,127,
        8,7,10,7,12,7,130,9,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,186,8,8,1,9,1,
        9,1,9,1,9,1,9,5,9,193,8,9,10,9,12,9,196,9,9,1,10,1,10,3,10,200,8,
        10,1,11,1,11,1,11,1,12,1,12,1,12,1,13,1,13,5,13,210,8,13,10,13,12,
        13,213,9,13,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,
        14,225,8,14,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,16,3,16,235,8,16,
        1,16,0,1,14,17,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,0,4,
        1,0,30,31,1,0,35,40,2,0,3,3,6,6,1,0,48,49,257,0,40,1,0,0,0,2,42,
        1,0,0,0,4,60,1,0,0,0,6,62,1,0,0,0,8,70,1,0,0,0,10,75,1,0,0,0,12,
        78,1,0,0,0,14,93,1,0,0,0,16,185,1,0,0,0,18,187,1,0,0,0,20,197,1,
        0,0,0,22,201,1,0,0,0,24,204,1,0,0,0,26,207,1,0,0,0,28,224,1,0,0,
        0,30,226,1,0,0,0,32,234,1,0,0,0,34,35,3,2,1,0,35,36,5,0,0,1,36,41,
        1,0,0,0,37,38,3,14,7,0,38,39,5,0,0,1,39,41,1,0,0,0,40,34,1,0,0,0,
        40,37,1,0,0,0,41,1,1,0,0,0,42,43,3,4,2,0,43,45,3,10,5,0,44,46,3,
        12,6,0,45,44,1,0,0,0,45,46,1,0,0,0,46,48,1,0,0,0,47,49,3,18,9,0,
        48,47,1,0,0,0,48,49,1,0,0,0,49,51,1,0,0,0,50,52,3,22,11,0,51,50,
        1,0,0,0,51,52,1,0,0,0,52,54,1,0,0,0,53,55,3,24,12,0,54,53,1,0,0,
        0,54,55,1,0,0,0,55,3,1,0,0,0,56,57,5,16,0,0,57,61,5,32,0,0,58,59,
        5,16,0,0,59,61,3,6,3,0,60,56,1,0,0,0,60,58,1,0,0,0,61,5,1,0,0,0,
        62,67,3,8,4,0,63,64,5,29,0,0,64,66,3,8,4,0,65,63,1,0,0,0,66,69,1,
        0,0,0,67,65,1,0,0,0,67,68,1,0,0,0,68,7,1,0,0,0,69,67,1,0,0,0,70,
        73,3,14,7,0,71,72,5,2,0,0,72,74,3,26,13,0,73,71,1,0,0,0,73,74,1,
        0,0,0,74,9,1,0,0,0,75,76,5,8,0,0,76,77,3,26,13,0,77,11,1,0,0,0,78,
        79,5,19,0,0,79,80,3,14,7,0,80,13,1,0,0,0,81,82,6,7,-1,0,82,94,3,
        32,16,0,83,94,3,26,13,0,84,85,7,0,0,0,85,94,3,14,7,9,86,87,5,43,
        0,0,87,88,3,14,7,0,88,89,5,44,0,0,89,94,1,0,0,0,90,94,3,16,8,0,91,
        92,5,11,0,0,92,94,3,14,7,3,93,81,1,0,0,0,93,83,1,0,0,0,93,84,1,0,
        0,0,93,86,1,0,0,0,93,90,1,0,0,0,93,91,1,0,0,0,94,128,1,0,0,0,95,
        96,10,6,0,0,96,97,7,1,0,0,97,127,3,14,7,7,98,99,10,4,0,0,99,100,
        5,4,0,0,100,101,3,14,7,0,101,102,5,1,0,0,102,103,3,14,7,5,103,127,
        1,0,0,0,104,105,10,2,0,0,105,106,5,1,0,0,106,127,3,14,7,3,107,108,
        10,1,0,0,108,109,5,14,0,0,109,127,3,14,7,2,110,112,10,5,0,0,111,
        113,5,11,0,0,112,111,1,0,0,0,112,113,1,0,0,0,113,114,1,0,0,0,114,
        115,5,9,0,0,115,116,5,43,0,0,116,121,3,14,7,0,117,118,5,29,0,0,118,
        120,3,14,7,0,119,117,1,0,0,0,120,123,1,0,0,0,121,119,1,0,0,0,121,
        122,1,0,0,0,122,124,1,0,0,0,123,121,1,0,0,0,124,125,5,44,0,0,125,
        127,1,0,0,0,126,95,1,0,0,0,126,98,1,0,0,0,126,104,1,0,0,0,126,107,
        1,0,0,0,126,110,1,0,0,0,127,130,1,0,0,0,128,126,1,0,0,0,128,129,
        1,0,0,0,129,15,1,0,0,0,130,128,1,0,0,0,131,132,5,20,0,0,132,133,
        5,43,0,0,133,134,3,14,7,0,134,135,5,44,0,0,135,186,1,0,0,0,136,137,
        5,21,0,0,137,138,5,43,0,0,138,139,3,14,7,0,139,140,5,29,0,0,140,
        141,3,14,7,0,141,142,5,44,0,0,142,186,1,0,0,0,143,144,5,22,0,0,144,
        145,5,43,0,0,145,146,3,14,7,0,146,147,5,29,0,0,147,148,3,14,7,0,
        148,149,5,44,0,0,149,186,1,0,0,0,150,151,5,23,0,0,151,152,5,43,0,
        0,152,153,3,14,7,0,153,154,5,44,0,0,154,186,1,0,0,0,155,156,5,24,
        0,0,156,157,5,43,0,0,157,158,3,14,7,0,158,159,5,29,0,0,159,160,3,
        14,7,0,160,161,5,44,0,0,161,186,1,0,0,0,162,163,5,25,0,0,163,164,
        5,43,0,0,164,165,3,14,7,0,165,166,5,44,0,0,166,186,1,0,0,0,167,168,
        5,26,0,0,168,169,5,43,0,0,169,170,3,14,7,0,170,171,5,29,0,0,171,
        172,3,14,7,0,172,173,5,44,0,0,173,186,1,0,0,0,174,175,5,27,0,0,175,
        176,5,43,0,0,176,177,3,14,7,0,177,178,5,29,0,0,178,179,3,14,7,0,
        179,180,5,44,0,0,180,186,1,0,0,0,181,182,5,28,0,0,182,183,5,43,0,
        0,183,184,5,32,0,0,184,186,5,44,0,0,185,131,1,0,0,0,185,136,1,0,
        0,0,185,143,1,0,0,0,185,150,1,0,0,0,185,155,1,0,0,0,185,162,1,0,
        0,0,185,167,1,0,0,0,185,174,1,0,0,0,185,181,1,0,0,0,186,17,1,0,0,
        0,187,188,5,15,0,0,188,189,5,5,0,0,189,194,3,20,10,0,190,191,5,29,
        0,0,191,193,3,20,10,0,192,190,1,0,0,0,193,196,1,0,0,0,194,192,1,
        0,0,0,194,195,1,0,0,0,195,19,1,0,0,0,196,194,1,0,0,0,197,199,3,14,
        7,0,198,200,7,2,0,0,199,198,1,0,0,0,199,200,1,0,0,0,200,21,1,0,0,
        0,201,202,5,10,0,0,202,203,3,14,7,0,203,23,1,0,0,0,204,205,5,13,
        0,0,205,206,3,14,7,0,206,25,1,0,0,0,207,211,3,30,15,0,208,210,3,
        28,14,0,209,208,1,0,0,0,210,213,1,0,0,0,211,209,1,0,0,0,211,212,
        1,0,0,0,212,27,1,0,0,0,213,211,1,0,0,0,214,215,5,41,0,0,215,216,
        3,32,16,0,216,217,5,42,0,0,217,225,1,0,0,0,218,219,5,41,0,0,219,
        220,3,30,15,0,220,221,5,42,0,0,221,225,1,0,0,0,222,223,5,33,0,0,
        223,225,3,30,15,0,224,214,1,0,0,0,224,218,1,0,0,0,224,222,1,0,0,
        0,225,29,1,0,0,0,226,227,7,3,0,0,227,31,1,0,0,0,228,235,5,12,0,0,
        229,235,5,17,0,0,230,235,5,7,0,0,231,235,5,45,0,0,232,235,5,46,0,
        0,233,235,5,47,0,0,234,228,1,0,0,0,234,229,1,0,0,0,234,230,1,0,0,
        0,234,231,1,0,0,0,234,232,1,0,0,0,234,233,1,0,0,0,235,33,1,0,0,0,
        19,40,45,48,51,54,60,67,73,93,112,121,126,128,185,194,199,211,224,
        234
    ]

class VerseQLParser ( Parser ):

    grammarFileName = "VerseQLParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'AND'", "'AS'", "'ASC'", "'BETWEEN'", 
                     "'BY'", "'DESC'", "'FALSE'", "'FROM'", "'IN'", "'LIMIT'", 
                     "'NOT'", "'NULL'", "'OFFSET'", "'OR'", "'ORDER'", "'SELECT'", 
                     "'TRUE'", "'VALUE'", "'WHERE'", "'IS_DEFINED'", "'IS_TYPE'", 
                     "'ARRAY_CONTAINS'", "'ARRAY_LENGTH'", "'CONTAINS'", 
                     "'LENGTH'", "'STARTS_WITH'", "'ENDS_WITH'", "'COUNT'", 
                     "','", "'+'", "'-'", "'*'", "'.'", "'?'", "'<'", "'<='", 
                     "'>'", "'>='", "'='", "<INVALID>", "'['", "']'", "'('", 
                     "')'" ]

    symbolicNames = [ "<INVALID>", "AND", "AS", "ASC", "BETWEEN", "BY", 
                      "DESC", "FALSE", "FROM", "IN", "LIMIT", "NOT", "NULL", 
                      "OFFSET", "OR", "ORDER", "SELECT", "TRUE", "VALUE", 
                      "WHERE", "IS_DEFINED", "IS_TYPE", "ARRAY_CONTAINS", 
                      "ARRAY_LENGTH", "CONTAINS", "LENGTH", "STARTS_WITH", 
                      "ENDS_WITH", "COUNT", "COMMA", "PLUS", "MINUS", "STAR", 
                      "DOT", "QUESTION_MARK", "LT", "LT_EQ", "GT", "GT_EQ", 
                      "EQ", "NEQ", "BRACKET_LEFT", "BRACKET_RIGHT", "PAREN_LEFT", 
                      "PAREN_RIGHT", "LITERAL_STRING", "LITERAL_INTEGER", 
                      "LITERAL_DECIMAL", "IDENTIFIER", "IDENTIFIER_QUOTED", 
                      "WS", "COMMENT_SINGLE_LINE", "COMMENT_MULTILINE", 
                      "UNRECOGNIZED" ]

    RULE_parse = 0
    RULE_query = 1
    RULE_select_clause = 2
    RULE_projection = 3
    RULE_projection_item = 4
    RULE_from_clause = 5
    RULE_where_clause = 6
    RULE_expression = 7
    RULE_function = 8
    RULE_order_by_clause = 9
    RULE_order_term = 10
    RULE_limit_clause = 11
    RULE_offset_clause = 12
    RULE_identifier = 13
    RULE_identifier_path = 14
    RULE_identifier_primitive = 15
    RULE_literal = 16

    ruleNames =  [ "parse", "query", "select_clause", "projection", "projection_item", 
                   "from_clause", "where_clause", "expression", "function", 
                   "order_by_clause", "order_term", "limit_clause", "offset_clause", 
                   "identifier", "identifier_path", "identifier_primitive", 
                   "literal" ]

    EOF = Token.EOF
    AND=1
    AS=2
    ASC=3
    BETWEEN=4
    BY=5
    DESC=6
    FALSE=7
    FROM=8
    IN=9
    LIMIT=10
    NOT=11
    NULL=12
    OFFSET=13
    OR=14
    ORDER=15
    SELECT=16
    TRUE=17
    VALUE=18
    WHERE=19
    IS_DEFINED=20
    IS_TYPE=21
    ARRAY_CONTAINS=22
    ARRAY_LENGTH=23
    CONTAINS=24
    LENGTH=25
    STARTS_WITH=26
    ENDS_WITH=27
    COUNT=28
    COMMA=29
    PLUS=30
    MINUS=31
    STAR=32
    DOT=33
    QUESTION_MARK=34
    LT=35
    LT_EQ=36
    GT=37
    GT_EQ=38
    EQ=39
    NEQ=40
    BRACKET_LEFT=41
    BRACKET_RIGHT=42
    PAREN_LEFT=43
    PAREN_RIGHT=44
    LITERAL_STRING=45
    LITERAL_INTEGER=46
    LITERAL_DECIMAL=47
    IDENTIFIER=48
    IDENTIFIER_QUOTED=49
    WS=50
    COMMENT_SINGLE_LINE=51
    COMMENT_MULTILINE=52
    UNRECOGNIZED=53

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_parse

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Parse_expressionContext(ParseContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ParseContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)

        def EOF(self):
            return self.getToken(VerseQLParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParse_expression" ):
                listener.enterParse_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParse_expression" ):
                listener.exitParse_expression(self)


    class Parse_queryContext(ParseContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ParseContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def query(self):
            return self.getTypedRuleContext(VerseQLParser.QueryContext,0)

        def EOF(self):
            return self.getToken(VerseQLParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParse_query" ):
                listener.enterParse_query(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParse_query" ):
                listener.exitParse_query(self)



    def parse(self):

        localctx = VerseQLParser.ParseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parse)
        try:
            self.state = 40
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16]:
                localctx = VerseQLParser.Parse_queryContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.query()
                self.state = 35
                self.match(VerseQLParser.EOF)
                pass
            elif token in [7, 11, 12, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 43, 45, 46, 47, 48, 49]:
                localctx = VerseQLParser.Parse_expressionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 37
                self.expression(0)
                self.state = 38
                self.match(VerseQLParser.EOF)
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


    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def select_clause(self):
            return self.getTypedRuleContext(VerseQLParser.Select_clauseContext,0)


        def from_clause(self):
            return self.getTypedRuleContext(VerseQLParser.From_clauseContext,0)


        def where_clause(self):
            return self.getTypedRuleContext(VerseQLParser.Where_clauseContext,0)


        def order_by_clause(self):
            return self.getTypedRuleContext(VerseQLParser.Order_by_clauseContext,0)


        def limit_clause(self):
            return self.getTypedRuleContext(VerseQLParser.Limit_clauseContext,0)


        def offset_clause(self):
            return self.getTypedRuleContext(VerseQLParser.Offset_clauseContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)




    def query(self):

        localctx = VerseQLParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.select_clause()
            self.state = 43
            self.from_clause()
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 44
                self.where_clause()


            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==15:
                self.state = 47
                self.order_by_clause()


            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 50
                self.limit_clause()


            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 53
                self.offset_clause()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Select_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_select_clause

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Select_itemsContext(Select_clauseContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.Select_clauseContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SELECT(self):
            return self.getToken(VerseQLParser.SELECT, 0)
        def projection(self):
            return self.getTypedRuleContext(VerseQLParser.ProjectionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelect_items" ):
                listener.enterSelect_items(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelect_items" ):
                listener.exitSelect_items(self)


    class Select_allContext(Select_clauseContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.Select_clauseContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SELECT(self):
            return self.getToken(VerseQLParser.SELECT, 0)
        def STAR(self):
            return self.getToken(VerseQLParser.STAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelect_all" ):
                listener.enterSelect_all(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelect_all" ):
                listener.exitSelect_all(self)



    def select_clause(self):

        localctx = VerseQLParser.Select_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_select_clause)
        try:
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                localctx = VerseQLParser.Select_allContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.match(VerseQLParser.SELECT)
                self.state = 57
                self.match(VerseQLParser.STAR)
                pass

            elif la_ == 2:
                localctx = VerseQLParser.Select_itemsContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.match(VerseQLParser.SELECT)
                self.state = 59
                self.projection()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProjectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def projection_item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.Projection_itemContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.Projection_itemContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(VerseQLParser.COMMA)
            else:
                return self.getToken(VerseQLParser.COMMA, i)

        def getRuleIndex(self):
            return VerseQLParser.RULE_projection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjection" ):
                listener.enterProjection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjection" ):
                listener.exitProjection(self)




    def projection(self):

        localctx = VerseQLParser.ProjectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_projection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.projection_item()
            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 63
                self.match(VerseQLParser.COMMA)
                self.state = 64
                self.projection_item()
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Projection_itemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def AS(self):
            return self.getToken(VerseQLParser.AS, 0)

        def identifier(self):
            return self.getTypedRuleContext(VerseQLParser.IdentifierContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_projection_item

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjection_item" ):
                listener.enterProjection_item(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjection_item" ):
                listener.exitProjection_item(self)




    def projection_item(self):

        localctx = VerseQLParser.Projection_itemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_projection_item)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.expression(0)
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 71
                self.match(VerseQLParser.AS)
                self.state = 72
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class From_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(VerseQLParser.FROM, 0)

        def identifier(self):
            return self.getTypedRuleContext(VerseQLParser.IdentifierContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_from_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFrom_clause" ):
                listener.enterFrom_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFrom_clause" ):
                listener.exitFrom_clause(self)




    def from_clause(self):

        localctx = VerseQLParser.From_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_from_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(VerseQLParser.FROM)
            self.state = 76
            self.identifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Where_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHERE(self):
            return self.getToken(VerseQLParser.WHERE, 0)

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_where_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhere_clause" ):
                listener.enterWhere_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhere_clause" ):
                listener.exitWhere_clause(self)




    def where_clause(self):

        localctx = VerseQLParser.Where_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_where_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(VerseQLParser.WHERE)
            self.state = 79
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Expression_unaryContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.sign = None # Token
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)

        def PLUS(self):
            return self.getToken(VerseQLParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(VerseQLParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_unary" ):
                listener.enterExpression_unary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_unary" ):
                listener.exitExpression_unary(self)


    class Expression_notContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(VerseQLParser.NOT, 0)
        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_not" ):
                listener.enterExpression_not(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_not" ):
                listener.exitExpression_not(self)


    class Expression_predicate_comparisonContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.lexpr = None # ExpressionContext
            self.op = None # Token
            self.rexpr = None # ExpressionContext
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)

        def EQ(self):
            return self.getToken(VerseQLParser.EQ, 0)
        def NEQ(self):
            return self.getToken(VerseQLParser.NEQ, 0)
        def GT(self):
            return self.getToken(VerseQLParser.GT, 0)
        def GT_EQ(self):
            return self.getToken(VerseQLParser.GT_EQ, 0)
        def LT(self):
            return self.getToken(VerseQLParser.LT, 0)
        def LT_EQ(self):
            return self.getToken(VerseQLParser.LT_EQ, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_predicate_comparison" ):
                listener.enterExpression_predicate_comparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_predicate_comparison" ):
                listener.exitExpression_predicate_comparison(self)


    class Expression_orContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.lexpr = None # ExpressionContext
            self.rexpr = None # ExpressionContext
            self.copyFrom(ctx)

        def OR(self):
            return self.getToken(VerseQLParser.OR, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_or" ):
                listener.enterExpression_or(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_or" ):
                listener.exitExpression_or(self)


    class Expression_primitive_identifierContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def identifier(self):
            return self.getTypedRuleContext(VerseQLParser.IdentifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_primitive_identifier" ):
                listener.enterExpression_primitive_identifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_primitive_identifier" ):
                listener.exitExpression_primitive_identifier(self)


    class Expression_predicate_inContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.expr = None # ExpressionContext
            self.not_in = None # Token
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(VerseQLParser.IN, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)

        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(VerseQLParser.COMMA)
            else:
                return self.getToken(VerseQLParser.COMMA, i)
        def NOT(self):
            return self.getToken(VerseQLParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_predicate_in" ):
                listener.enterExpression_predicate_in(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_predicate_in" ):
                listener.exitExpression_predicate_in(self)


    class Expression_functionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def function(self):
            return self.getTypedRuleContext(VerseQLParser.FunctionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_function" ):
                listener.enterExpression_function(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_function" ):
                listener.exitExpression_function(self)


    class Expression_paranthesisContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)

        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_paranthesis" ):
                listener.enterExpression_paranthesis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_paranthesis" ):
                listener.exitExpression_paranthesis(self)


    class Expression_andContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.lexpr = None # ExpressionContext
            self.rexpr = None # ExpressionContext
            self.copyFrom(ctx)

        def AND(self):
            return self.getToken(VerseQLParser.AND, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_and" ):
                listener.enterExpression_and(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_and" ):
                listener.exitExpression_and(self)


    class Expression_predicate_betweenContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.expr = None # ExpressionContext
            self.low = None # ExpressionContext
            self.high = None # ExpressionContext
            self.copyFrom(ctx)

        def BETWEEN(self):
            return self.getToken(VerseQLParser.BETWEEN, 0)
        def AND(self):
            return self.getToken(VerseQLParser.AND, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_predicate_between" ):
                listener.enterExpression_predicate_between(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_predicate_between" ):
                listener.exitExpression_predicate_between(self)


    class Expression_primitive_literalContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(VerseQLParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_primitive_literal" ):
                listener.enterExpression_primitive_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_primitive_literal" ):
                listener.exitExpression_primitive_literal(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = VerseQLParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 12, 17, 45, 46, 47]:
                localctx = VerseQLParser.Expression_primitive_literalContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 82
                self.literal()
                pass
            elif token in [48, 49]:
                localctx = VerseQLParser.Expression_primitive_identifierContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 83
                self.identifier()
                pass
            elif token in [30, 31]:
                localctx = VerseQLParser.Expression_unaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 84
                localctx.sign = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    localctx.sign = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 85
                self.expression(9)
                pass
            elif token in [43]:
                localctx = VerseQLParser.Expression_paranthesisContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 86
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 87
                self.expression(0)
                self.state = 88
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [20, 21, 22, 23, 24, 25, 26, 27, 28]:
                localctx = VerseQLParser.Expression_functionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 90
                self.function()
                pass
            elif token in [11]:
                localctx = VerseQLParser.Expression_notContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 91
                self.match(VerseQLParser.NOT)
                self.state = 92
                self.expression(3)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 128
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 126
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                    if la_ == 1:
                        localctx = VerseQLParser.Expression_predicate_comparisonContext(self, VerseQLParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.lexpr = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 95
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 96
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2164663517184) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 97
                        localctx.rexpr = self.expression(7)
                        pass

                    elif la_ == 2:
                        localctx = VerseQLParser.Expression_predicate_betweenContext(self, VerseQLParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.expr = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 98
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 99
                        self.match(VerseQLParser.BETWEEN)
                        self.state = 100
                        localctx.low = self.expression(0)
                        self.state = 101
                        self.match(VerseQLParser.AND)
                        self.state = 102
                        localctx.high = self.expression(5)
                        pass

                    elif la_ == 3:
                        localctx = VerseQLParser.Expression_andContext(self, VerseQLParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.lexpr = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 104
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 105
                        self.match(VerseQLParser.AND)
                        self.state = 106
                        localctx.rexpr = self.expression(3)
                        pass

                    elif la_ == 4:
                        localctx = VerseQLParser.Expression_orContext(self, VerseQLParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.lexpr = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 107
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 108
                        self.match(VerseQLParser.OR)
                        self.state = 109
                        localctx.rexpr = self.expression(2)
                        pass

                    elif la_ == 5:
                        localctx = VerseQLParser.Expression_predicate_inContext(self, VerseQLParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.expr = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 110
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 112
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==11:
                            self.state = 111
                            localctx.not_in = self.match(VerseQLParser.NOT)


                        self.state = 114
                        self.match(VerseQLParser.IN)
                        self.state = 115
                        self.match(VerseQLParser.PAREN_LEFT)
                        self.state = 116
                        self.expression(0)
                        self.state = 121
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==29:
                            self.state = 117
                            self.match(VerseQLParser.COMMA)
                            self.state = 118
                            self.expression(0)
                            self.state = 123
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 124
                        self.match(VerseQLParser.PAREN_RIGHT)
                        pass

             
                self.state = 130
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_function

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Function_count_allContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def COUNT(self):
            return self.getToken(VerseQLParser.COUNT, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def STAR(self):
            return self.getToken(VerseQLParser.STAR, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_count_all" ):
                listener.enterFunction_count_all(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_count_all" ):
                listener.exitFunction_count_all(self)


    class Function_starts_withContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.p1 = None # ExpressionContext
            self.copyFrom(ctx)

        def STARTS_WITH(self):
            return self.getToken(VerseQLParser.STARTS_WITH, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def COMMA(self):
            return self.getToken(VerseQLParser.COMMA, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_starts_with" ):
                listener.enterFunction_starts_with(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_starts_with" ):
                listener.exitFunction_starts_with(self)


    class Function_ends_withContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.p1 = None # ExpressionContext
            self.copyFrom(ctx)

        def ENDS_WITH(self):
            return self.getToken(VerseQLParser.ENDS_WITH, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def COMMA(self):
            return self.getToken(VerseQLParser.COMMA, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_ends_with" ):
                listener.enterFunction_ends_with(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_ends_with" ):
                listener.exitFunction_ends_with(self)


    class Function_array_containsContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.p1 = None # ExpressionContext
            self.copyFrom(ctx)

        def ARRAY_CONTAINS(self):
            return self.getToken(VerseQLParser.ARRAY_CONTAINS, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def COMMA(self):
            return self.getToken(VerseQLParser.COMMA, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_array_contains" ):
                listener.enterFunction_array_contains(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_array_contains" ):
                listener.exitFunction_array_contains(self)


    class Function_array_lengthContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.copyFrom(ctx)

        def ARRAY_LENGTH(self):
            return self.getToken(VerseQLParser.ARRAY_LENGTH, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_array_length" ):
                listener.enterFunction_array_length(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_array_length" ):
                listener.exitFunction_array_length(self)


    class Function_lengthContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.copyFrom(ctx)

        def LENGTH(self):
            return self.getToken(VerseQLParser.LENGTH, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_length" ):
                listener.enterFunction_length(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_length" ):
                listener.exitFunction_length(self)


    class Function_containsContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.p1 = None # ExpressionContext
            self.copyFrom(ctx)

        def CONTAINS(self):
            return self.getToken(VerseQLParser.CONTAINS, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def COMMA(self):
            return self.getToken(VerseQLParser.COMMA, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_contains" ):
                listener.enterFunction_contains(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_contains" ):
                listener.exitFunction_contains(self)


    class Function_is_definedContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.copyFrom(ctx)

        def IS_DEFINED(self):
            return self.getToken(VerseQLParser.IS_DEFINED, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_is_defined" ):
                listener.enterFunction_is_defined(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_is_defined" ):
                listener.exitFunction_is_defined(self)


    class Function_is_typeContext(FunctionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.FunctionContext
            super().__init__(parser)
            self.p0 = None # ExpressionContext
            self.p1 = None # ExpressionContext
            self.copyFrom(ctx)

        def IS_TYPE(self):
            return self.getToken(VerseQLParser.IS_TYPE, 0)
        def PAREN_LEFT(self):
            return self.getToken(VerseQLParser.PAREN_LEFT, 0)
        def COMMA(self):
            return self.getToken(VerseQLParser.COMMA, 0)
        def PAREN_RIGHT(self):
            return self.getToken(VerseQLParser.PAREN_RIGHT, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_is_type" ):
                listener.enterFunction_is_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_is_type" ):
                listener.exitFunction_is_type(self)



    def function(self):

        localctx = VerseQLParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_function)
        try:
            self.state = 185
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                localctx = VerseQLParser.Function_is_definedContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self.match(VerseQLParser.IS_DEFINED)
                self.state = 132
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 133
                localctx.p0 = self.expression(0)
                self.state = 134
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [21]:
                localctx = VerseQLParser.Function_is_typeContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 136
                self.match(VerseQLParser.IS_TYPE)
                self.state = 137
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 138
                localctx.p0 = self.expression(0)
                self.state = 139
                self.match(VerseQLParser.COMMA)
                self.state = 140
                localctx.p1 = self.expression(0)
                self.state = 141
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [22]:
                localctx = VerseQLParser.Function_array_containsContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 143
                self.match(VerseQLParser.ARRAY_CONTAINS)
                self.state = 144
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 145
                localctx.p0 = self.expression(0)
                self.state = 146
                self.match(VerseQLParser.COMMA)
                self.state = 147
                localctx.p1 = self.expression(0)
                self.state = 148
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [23]:
                localctx = VerseQLParser.Function_array_lengthContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 150
                self.match(VerseQLParser.ARRAY_LENGTH)
                self.state = 151
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 152
                localctx.p0 = self.expression(0)
                self.state = 153
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [24]:
                localctx = VerseQLParser.Function_containsContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 155
                self.match(VerseQLParser.CONTAINS)
                self.state = 156
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 157
                localctx.p0 = self.expression(0)
                self.state = 158
                self.match(VerseQLParser.COMMA)
                self.state = 159
                localctx.p1 = self.expression(0)
                self.state = 160
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [25]:
                localctx = VerseQLParser.Function_lengthContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 162
                self.match(VerseQLParser.LENGTH)
                self.state = 163
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 164
                localctx.p0 = self.expression(0)
                self.state = 165
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [26]:
                localctx = VerseQLParser.Function_starts_withContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 167
                self.match(VerseQLParser.STARTS_WITH)
                self.state = 168
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 169
                localctx.p0 = self.expression(0)
                self.state = 170
                self.match(VerseQLParser.COMMA)
                self.state = 171
                localctx.p1 = self.expression(0)
                self.state = 172
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [27]:
                localctx = VerseQLParser.Function_ends_withContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 174
                self.match(VerseQLParser.ENDS_WITH)
                self.state = 175
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 176
                localctx.p0 = self.expression(0)
                self.state = 177
                self.match(VerseQLParser.COMMA)
                self.state = 178
                localctx.p1 = self.expression(0)
                self.state = 179
                self.match(VerseQLParser.PAREN_RIGHT)
                pass
            elif token in [28]:
                localctx = VerseQLParser.Function_count_allContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 181
                self.match(VerseQLParser.COUNT)
                self.state = 182
                self.match(VerseQLParser.PAREN_LEFT)
                self.state = 183
                self.match(VerseQLParser.STAR)
                self.state = 184
                self.match(VerseQLParser.PAREN_RIGHT)
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


    class Order_by_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ORDER(self):
            return self.getToken(VerseQLParser.ORDER, 0)

        def BY(self):
            return self.getToken(VerseQLParser.BY, 0)

        def order_term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.Order_termContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.Order_termContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(VerseQLParser.COMMA)
            else:
                return self.getToken(VerseQLParser.COMMA, i)

        def getRuleIndex(self):
            return VerseQLParser.RULE_order_by_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrder_by_clause" ):
                listener.enterOrder_by_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrder_by_clause" ):
                listener.exitOrder_by_clause(self)




    def order_by_clause(self):

        localctx = VerseQLParser.Order_by_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_order_by_clause)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 187
            self.match(VerseQLParser.ORDER)
            self.state = 188
            self.match(VerseQLParser.BY)
            self.state = 189
            self.order_term()
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 190
                self.match(VerseQLParser.COMMA)
                self.state = 191
                self.order_term()
                self.state = 196
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Order_termContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.direction = None # Token

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def ASC(self):
            return self.getToken(VerseQLParser.ASC, 0)

        def DESC(self):
            return self.getToken(VerseQLParser.DESC, 0)

        def getRuleIndex(self):
            return VerseQLParser.RULE_order_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrder_term" ):
                listener.enterOrder_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrder_term" ):
                listener.exitOrder_term(self)




    def order_term(self):

        localctx = VerseQLParser.Order_termContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_order_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.expression(0)
            self.state = 199
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3 or _la==6:
                self.state = 198
                localctx.direction = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==3 or _la==6):
                    localctx.direction = self._errHandler.recoverInline(self)
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


    class Limit_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LIMIT(self):
            return self.getToken(VerseQLParser.LIMIT, 0)

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_limit_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLimit_clause" ):
                listener.enterLimit_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLimit_clause" ):
                listener.exitLimit_clause(self)




    def limit_clause(self):

        localctx = VerseQLParser.Limit_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_limit_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self.match(VerseQLParser.LIMIT)
            self.state = 202
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Offset_clauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OFFSET(self):
            return self.getToken(VerseQLParser.OFFSET, 0)

        def expression(self):
            return self.getTypedRuleContext(VerseQLParser.ExpressionContext,0)


        def getRuleIndex(self):
            return VerseQLParser.RULE_offset_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOffset_clause" ):
                listener.enterOffset_clause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOffset_clause" ):
                listener.exitOffset_clause(self)




    def offset_clause(self):

        localctx = VerseQLParser.Offset_clauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_offset_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.match(VerseQLParser.OFFSET)
            self.state = 205
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier_primitive(self):
            return self.getTypedRuleContext(VerseQLParser.Identifier_primitiveContext,0)


        def identifier_path(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VerseQLParser.Identifier_pathContext)
            else:
                return self.getTypedRuleContext(VerseQLParser.Identifier_pathContext,i)


        def getRuleIndex(self):
            return VerseQLParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)




    def identifier(self):

        localctx = VerseQLParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.identifier_primitive()
            self.state = 211
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 208
                    self.identifier_path() 
                self.state = 213
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Identifier_pathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_identifier_path

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Identifier_path_array_primitiveContext(Identifier_pathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.Identifier_pathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BRACKET_LEFT(self):
            return self.getToken(VerseQLParser.BRACKET_LEFT, 0)
        def identifier_primitive(self):
            return self.getTypedRuleContext(VerseQLParser.Identifier_primitiveContext,0)

        def BRACKET_RIGHT(self):
            return self.getToken(VerseQLParser.BRACKET_RIGHT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier_path_array_primitive" ):
                listener.enterIdentifier_path_array_primitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier_path_array_primitive" ):
                listener.exitIdentifier_path_array_primitive(self)


    class Identifier_path_literalContext(Identifier_pathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.Identifier_pathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BRACKET_LEFT(self):
            return self.getToken(VerseQLParser.BRACKET_LEFT, 0)
        def literal(self):
            return self.getTypedRuleContext(VerseQLParser.LiteralContext,0)

        def BRACKET_RIGHT(self):
            return self.getToken(VerseQLParser.BRACKET_RIGHT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier_path_literal" ):
                listener.enterIdentifier_path_literal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier_path_literal" ):
                listener.exitIdentifier_path_literal(self)


    class Identifier_path_dot_primitiveContext(Identifier_pathContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.Identifier_pathContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DOT(self):
            return self.getToken(VerseQLParser.DOT, 0)
        def identifier_primitive(self):
            return self.getTypedRuleContext(VerseQLParser.Identifier_primitiveContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier_path_dot_primitive" ):
                listener.enterIdentifier_path_dot_primitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier_path_dot_primitive" ):
                listener.exitIdentifier_path_dot_primitive(self)



    def identifier_path(self):

        localctx = VerseQLParser.Identifier_pathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_identifier_path)
        try:
            self.state = 224
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                localctx = VerseQLParser.Identifier_path_literalContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 214
                self.match(VerseQLParser.BRACKET_LEFT)
                self.state = 215
                self.literal()
                self.state = 216
                self.match(VerseQLParser.BRACKET_RIGHT)
                pass

            elif la_ == 2:
                localctx = VerseQLParser.Identifier_path_array_primitiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 218
                self.match(VerseQLParser.BRACKET_LEFT)
                self.state = 219
                self.identifier_primitive()
                self.state = 220
                self.match(VerseQLParser.BRACKET_RIGHT)
                pass

            elif la_ == 3:
                localctx = VerseQLParser.Identifier_path_dot_primitiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 222
                self.match(VerseQLParser.DOT)
                self.state = 223
                self.identifier_primitive()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Identifier_primitiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(VerseQLParser.IDENTIFIER, 0)

        def IDENTIFIER_QUOTED(self):
            return self.getToken(VerseQLParser.IDENTIFIER_QUOTED, 0)

        def getRuleIndex(self):
            return VerseQLParser.RULE_identifier_primitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier_primitive" ):
                listener.enterIdentifier_primitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier_primitive" ):
                listener.exitIdentifier_primitive(self)




    def identifier_primitive(self):

        localctx = VerseQLParser.Identifier_primitiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_identifier_primitive)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 226
            _la = self._input.LA(1)
            if not(_la==48 or _la==49):
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


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return VerseQLParser.RULE_literal

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Literal_falseContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(VerseQLParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_false" ):
                listener.enterLiteral_false(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_false" ):
                listener.exitLiteral_false(self)


    class Literal_integerContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LITERAL_INTEGER(self):
            return self.getToken(VerseQLParser.LITERAL_INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_integer" ):
                listener.enterLiteral_integer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_integer" ):
                listener.exitLiteral_integer(self)


    class Literal_nullContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NULL(self):
            return self.getToken(VerseQLParser.NULL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_null" ):
                listener.enterLiteral_null(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_null" ):
                listener.exitLiteral_null(self)


    class Literal_decimalContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LITERAL_DECIMAL(self):
            return self.getToken(VerseQLParser.LITERAL_DECIMAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_decimal" ):
                listener.enterLiteral_decimal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_decimal" ):
                listener.exitLiteral_decimal(self)


    class Literal_trueContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(VerseQLParser.TRUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_true" ):
                listener.enterLiteral_true(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_true" ):
                listener.exitLiteral_true(self)


    class Literal_stringContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a VerseQLParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LITERAL_STRING(self):
            return self.getToken(VerseQLParser.LITERAL_STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral_string" ):
                listener.enterLiteral_string(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral_string" ):
                listener.exitLiteral_string(self)



    def literal(self):

        localctx = VerseQLParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_literal)
        try:
            self.state = 234
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                localctx = VerseQLParser.Literal_nullContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 228
                self.match(VerseQLParser.NULL)
                pass
            elif token in [17]:
                localctx = VerseQLParser.Literal_trueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 229
                self.match(VerseQLParser.TRUE)
                pass
            elif token in [7]:
                localctx = VerseQLParser.Literal_falseContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 230
                self.match(VerseQLParser.FALSE)
                pass
            elif token in [45]:
                localctx = VerseQLParser.Literal_stringContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 231
                self.match(VerseQLParser.LITERAL_STRING)
                pass
            elif token in [46]:
                localctx = VerseQLParser.Literal_integerContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 232
                self.match(VerseQLParser.LITERAL_INTEGER)
                pass
            elif token in [47]:
                localctx = VerseQLParser.Literal_decimalContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 233
                self.match(VerseQLParser.LITERAL_DECIMAL)
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



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[7] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         
