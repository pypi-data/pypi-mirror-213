from antlr4 import CommonTokenStream  # type: ignore
from antlr4 import InputStream  # type: ignore
from antlr4 import ParseTreeWalker  # type: ignore
from antlr4.error.ErrorListener import ErrorListener, ConsoleErrorListener

from ._expression import Expression
from ._parser_listener import VerseQLParserListener  # type: ignore
from ._query import Query
from .generated.VerseQLLexer import VerseQLLexer  # type: ignore
from .generated.VerseQLParser import VerseQLParser  # type: ignore


class VerseQL:
    @staticmethod
    def parse_query(query: str) -> Query:
        listener = VerseQL._parse(str=query)
        return listener.query

    @staticmethod
    def parse_expression(expr: str) -> Expression:
        listener = VerseQL._parse(str=expr)
        return listener.expression

    @staticmethod
    def _parse(str: str) -> VerseQLParserListener:
        input_stream = InputStream(str)
        lexer = VerseQLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = VerseQLParser(stream)
        parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
        parser.addErrorListener(ParserErrorListener())
        tree = parser.parse()
        listener = VerseQLParserListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener


class ParserErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ValueError("line " + str(line) + ":" + str(column) + " " + msg)

    def reportAmbiguity(
        self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
    ):
        pass

    def reportAttemptingFullContext(
        self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
    ):
        pass

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):
        pass
