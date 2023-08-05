# flake8: noqa
# type: ignore
# Generated from verseql/grammar/VerseQLParser.g4 by ANTLR 4.13.0
from antlr4 import *

from ._expression import (
    Primitive,
    Predicate,
    PredicateOp,
    Function,
    FunctionName,
    And,
    Or,
    Not,
)
from ._order import Order, OrderTerm
from ._projection import Projection, ProjectionItem

from ._query import Query
from .generated.VerseQLParser import VerseQLParser


# This class defines a complete listener for a parse tree produced by VerseQLParser.
class VerseQLParserListener(ParseTreeListener):
    query = None
    expression = None

    # Enter a parse tree produced by VerseQLParser#parse_query.
    def enterParse_query(self, ctx: VerseQLParser.Parse_queryContext):
        pass

    # Exit a parse tree produced by VerseQLParser#parse_query.
    def exitParse_query(self, ctx: VerseQLParser.Parse_queryContext):
        self.query = ctx.query().value

    # Enter a parse tree produced by VerseQLParser#parse_expression.
    def enterParse_expression(
        self, ctx: VerseQLParser.Parse_expressionContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#parse_expression.
    def exitParse_expression(self, ctx: VerseQLParser.Parse_expressionContext):
        self.expression = ctx.expression().value

    # Enter a parse tree produced by VerseQLParser#query.
    def enterQuery(self, ctx: VerseQLParser.QueryContext):
        pass

    # Exit a parse tree produced by VerseQLParser#query.
    def exitQuery(self, ctx: VerseQLParser.QueryContext):
        projection = ctx.select_clause().value
        store = ctx.from_clause().value
        filter = ctx.where_clause()
        order = ctx.order_by_clause()
        limit = ctx.limit_clause()
        offset = ctx.offset_clause()
        ctx.value = Query(
            projection=projection,
            store=store,
            filter=None if filter is None else filter.value,
            order=None if order is None else order.value,
            limit=None if limit is None else limit.value,
            offset=None if offset is None else offset.value,
        )
        self.query = ctx.value

    # Enter a parse tree produced by VerseQLParser#select_all.
    def enterSelect_all(self, ctx: VerseQLParser.Select_allContext):
        pass

    # Exit a parse tree produced by VerseQLParser#select_all.
    def exitSelect_all(self, ctx: VerseQLParser.Select_allContext):
        ctx.value = Projection()

    # Enter a parse tree produced by VerseQLParser#select_items.
    def enterSelect_items(self, ctx: VerseQLParser.Select_itemsContext):
        pass

    # Exit a parse tree produced by VerseQLParser#select_items.
    def exitSelect_items(self, ctx: VerseQLParser.Select_itemsContext):
        ctx.value = ctx.projection().value

    # Enter a parse tree produced by VerseQLParser#projection.
    def enterProjection(self, ctx: VerseQLParser.ProjectionContext):
        pass

    # Exit a parse tree produced by VerseQLParser#projection.
    def exitProjection(self, ctx: VerseQLParser.ProjectionContext):
        ctx.value = Projection(*(item.value for item in ctx.projection_item()))

    # Enter a parse tree produced by VerseQLParser#projection_item.
    def enterProjection_item(self, ctx: VerseQLParser.Projection_itemContext):
        pass

    # Exit a parse tree produced by VerseQLParser#projection_item.
    def exitProjection_item(self, ctx: VerseQLParser.Projection_itemContext):
        identifier = ctx.identifier()
        ctx.value = ProjectionItem(
            expr=ctx.expression().value,
            as_identifier=None if identifier is None else identifier.value,
        )

    # Enter a parse tree produced by VerseQLParser#from_clause.
    def enterFrom_clause(self, ctx: VerseQLParser.From_clauseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#from_clause.
    def exitFrom_clause(self, ctx: VerseQLParser.From_clauseContext):
        ctx.value = ctx.identifier().value

    # Enter a parse tree produced by VerseQLParser#where_clause.
    def enterWhere_clause(self, ctx: VerseQLParser.Where_clauseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#where_clause.
    def exitWhere_clause(self, ctx: VerseQLParser.Where_clauseContext):
        ctx.value = ctx.expression().value

    # Enter a parse tree produced by VerseQLParser#expression_unary.
    def enterExpression_unary(
        self, ctx: VerseQLParser.Expression_unaryContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_unary.
    def exitExpression_unary(self, ctx: VerseQLParser.Expression_unaryContext):
        expr = ctx.expression().value
        if (
            ctx.sign.text == "-"
            and isinstance(expr, Primitive)
            and isinstance(expr._expr, (int, float))
        ):
            expr = Primitive(expr=expr._expr * -1)
        ctx.value = expr

    # Enter a parse tree produced by VerseQLParser#expression_not.
    def enterExpression_not(self, ctx: VerseQLParser.Expression_notContext):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_not.
    def exitExpression_not(self, ctx: VerseQLParser.Expression_notContext):
        ctx.value = Not(ctx.expression().value)

    # Enter a parse tree produced by VerseQLParser#expression_predicate_comparison.
    def enterExpression_predicate_comparison(
        self, ctx: VerseQLParser.Expression_predicate_comparisonContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_predicate_comparison.
    def exitExpression_predicate_comparison(
        self, ctx: VerseQLParser.Expression_predicate_comparisonContext
    ):
        ctx.value = Predicate(
            left_expr=ctx.lexpr.value,
            op=ctx.op.text,
            right_expr=ctx.rexpr.value,
        )

    # Enter a parse tree produced by VerseQLParser#expression_or.
    def enterExpression_or(self, ctx: VerseQLParser.Expression_orContext):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_or.
    def exitExpression_or(self, ctx: VerseQLParser.Expression_orContext):
        ctx.value = Or(left_expr=ctx.lexpr.value, right_expr=ctx.rexpr.value)

    # Enter a parse tree produced by VerseQLParser#expression_primitive_identifier.
    def enterExpression_primitive_identifier(
        self, ctx: VerseQLParser.Expression_primitive_identifierContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_primitive_identifier.
    def exitExpression_primitive_identifier(
        self, ctx: VerseQLParser.Expression_primitive_identifierContext
    ):
        ctx.value = Primitive(ctx.identifier().value)

    # Enter a parse tree produced by VerseQLParser#expression_predicate_in.
    def enterExpression_predicate_in(
        self, ctx: VerseQLParser.Expression_predicate_inContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_predicate_in.
    def exitExpression_predicate_in(
        self, ctx: VerseQLParser.Expression_predicate_inContext
    ):
        op = PredicateOp.IN if ctx.not_in is None else PredicateOp.NOT_IN
        args = ctx.expression()
        ctx.value = Predicate(
            left_expr=ctx.expr.value,
            op=op,
            right_expr=tuple([args[i].value for i in range(1, len(args))]),
        )

    # Enter a parse tree produced by VerseQLParser#expression_function.
    def enterExpression_function(
        self, ctx: VerseQLParser.Expression_functionContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_function.
    def exitExpression_function(
        self, ctx: VerseQLParser.Expression_functionContext
    ):
        ctx.value = ctx.function().value

    # Enter a parse tree produced by VerseQLParser#expression_paranthesis.
    def enterExpression_paranthesis(
        self, ctx: VerseQLParser.Expression_paranthesisContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_paranthesis.
    def exitExpression_paranthesis(
        self, ctx: VerseQLParser.Expression_paranthesisContext
    ):
        ctx.value = ctx.expression().value

    # Enter a parse tree produced by VerseQLParser#expression_and.
    def enterExpression_and(self, ctx: VerseQLParser.Expression_andContext):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_and.
    def exitExpression_and(self, ctx: VerseQLParser.Expression_andContext):
        ctx.value = And(left_expr=ctx.lexpr.value, right_expr=ctx.rexpr.value)

    # Enter a parse tree produced by VerseQLParser#expression_predicate_between.
    def enterExpression_predicate_between(
        self, ctx: VerseQLParser.Expression_predicate_betweenContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_predicate_between.
    def exitExpression_predicate_between(
        self, ctx: VerseQLParser.Expression_predicate_betweenContext
    ):
        ctx.value = Predicate(
            left_expr=ctx.expr.value,
            op=PredicateOp.BETWEEN,
            right_expr=(ctx.low.value, ctx.high.value),
        )

    # Enter a parse tree produced by VerseQLParser#expression_primitive_literal.
    def enterExpression_primitive_literal(
        self, ctx: VerseQLParser.Expression_primitive_literalContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#expression_primitive_literal.
    def exitExpression_primitive_literal(
        self, ctx: VerseQLParser.Expression_primitive_literalContext
    ):
        ctx.value = Primitive(ctx.literal().value)

    # Enter a parse tree produced by VerseQLParser#function_is_defined.
    def enterFunction_is_defined(
        self, ctx: VerseQLParser.Function_is_definedContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_is_defined.
    def exitFunction_is_defined(
        self, ctx: VerseQLParser.Function_is_definedContext
    ):
        ctx.value = Function(FunctionName.IS_DEFINED, ctx.p0.value)

    # Enter a parse tree produced by VerseQLParser#function_is_type.
    def enterFunction_is_type(
        self, ctx: VerseQLParser.Function_is_typeContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_is_type.
    def exitFunction_is_type(self, ctx: VerseQLParser.Function_is_typeContext):
        ctx.value = Function(FunctionName.IS_TYPE, ctx.p0.value, ctx.p1.value)

    # Enter a parse tree produced by VerseQLParser#function_array_contains.
    def enterFunction_array_contains(
        self, ctx: VerseQLParser.Function_array_containsContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_array_contains.
    def exitFunction_array_contains(
        self, ctx: VerseQLParser.Function_array_containsContext
    ):
        ctx.value = Function(
            FunctionName.ARRAY_CONTAINS, ctx.p0.value, ctx.p1.value
        )

    # Enter a parse tree produced by VerseQLParser#function_array_length.
    def enterFunction_array_length(
        self, ctx: VerseQLParser.Function_array_lengthContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_array_length.
    def exitFunction_array_length(
        self, ctx: VerseQLParser.Function_array_lengthContext
    ):
        ctx.value = Function(
            FunctionName.ARRAY_LENGTH, ctx.p0.value, ctx.p1.value
        )

    # Enter a parse tree produced by VerseQLParser#function_contains.
    def enterFunction_contains(
        self, ctx: VerseQLParser.Function_containsContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_contains.
    def exitFunction_contains(
        self, ctx: VerseQLParser.Function_containsContext
    ):
        ctx.value = Function(FunctionName.CONTAINS, ctx.p0.value, ctx.p1.value)

    # Enter a parse tree produced by VerseQLParser#function_length.
    def enterFunction_length(self, ctx: VerseQLParser.Function_lengthContext):
        pass

    # Exit a parse tree produced by VerseQLParser#function_length.
    def exitFunction_length(self, ctx: VerseQLParser.Function_lengthContext):
        ctx.value = Function(FunctionName.LENGTH, ctx.p0.value)

    # Enter a parse tree produced by VerseQLParser#function_starts_with.
    def enterFunction_starts_with(
        self, ctx: VerseQLParser.Function_starts_withContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_starts_with.
    def exitFunction_starts_with(
        self, ctx: VerseQLParser.Function_starts_withContext
    ):
        ctx.value = Function(
            FunctionName.STARTSWITH, ctx.p0.value, ctx.p1.value
        )

    # Enter a parse tree produced by VerseQLParser#function_ends_with.
    def enterFunction_ends_with(
        self, ctx: VerseQLParser.Function_ends_withContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_ends_with.
    def exitFunction_ends_with(
        self, ctx: VerseQLParser.Function_ends_withContext
    ):
        ctx.value = Function(FunctionName.ENDSWITH, ctx.p0.value, ctx.p1.value)

    # Enter a parse tree produced by VerseQLParser#function_count_all.
    def enterFunction_count_all(
        self, ctx: VerseQLParser.Function_count_allContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#function_count_all.
    def exitFunction_count_all(
        self, ctx: VerseQLParser.Function_count_allContext
    ):
        ctx.value = Function(FunctionName.COUNT, "*")

    # Enter a parse tree produced by VerseQLParser#order_by_clause.
    def enterOrder_by_clause(self, ctx: VerseQLParser.Order_by_clauseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#order_by_clause.
    def exitOrder_by_clause(self, ctx: VerseQLParser.Order_by_clauseContext):
        ctx.value = Order(*(term.value for term in ctx.order_term()))

    # Enter a parse tree produced by VerseQLParser#order_term.
    def enterOrder_term(self, ctx: VerseQLParser.Order_termContext):
        pass

    # Exit a parse tree produced by VerseQLParser#order_term.
    def exitOrder_term(self, ctx: VerseQLParser.Order_termContext):
        ctx.value = OrderTerm(
            expr=ctx.expression().value,
            direction=None if ctx.direction is None else ctx.direction.text,
        )

    # Enter a parse tree produced by VerseQLParser#limit_clause.
    def enterLimit_clause(self, ctx: VerseQLParser.Limit_clauseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#limit_clause.
    def exitLimit_clause(self, ctx: VerseQLParser.Limit_clauseContext):
        ctx.value = ctx.expression().value

    # Enter a parse tree produced by VerseQLParser#offset_clause.
    def enterOffset_clause(self, ctx: VerseQLParser.Offset_clauseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#offset_clause.
    def exitOffset_clause(self, ctx: VerseQLParser.Offset_clauseContext):
        ctx.value = ctx.expression().value

    # Enter a parse tree produced by VerseQLParser#identifier.
    def enterIdentifier(self, ctx: VerseQLParser.IdentifierContext):
        pass

    # Exit a parse tree produced by VerseQLParser#identifier.
    def exitIdentifier(self, ctx: VerseQLParser.IdentifierContext):
        ctx.value = ctx.getText()

    # Enter a parse tree produced by VerseQLParser#identifier_path_literal.
    def enterIdentifier_path_literal(
        self, ctx: VerseQLParser.Identifier_path_literalContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#identifier_path_literal.
    def exitIdentifier_path_literal(
        self, ctx: VerseQLParser.Identifier_path_literalContext
    ):
        pass

    # Enter a parse tree produced by VerseQLParser#identifier_path_array_primitive.
    def enterIdentifier_path_array_primitive(
        self, ctx: VerseQLParser.Identifier_path_array_primitiveContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#identifier_path_array_primitive.
    def exitIdentifier_path_array_primitive(
        self, ctx: VerseQLParser.Identifier_path_array_primitiveContext
    ):
        pass

    # Enter a parse tree produced by VerseQLParser#identifier_path_dot_primitive.
    def enterIdentifier_path_dot_primitive(
        self, ctx: VerseQLParser.Identifier_path_dot_primitiveContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#identifier_path_dot_primitive.
    def exitIdentifier_path_dot_primitive(
        self, ctx: VerseQLParser.Identifier_path_dot_primitiveContext
    ):
        pass

    # Enter a parse tree produced by VerseQLParser#identifier_primitive.
    def enterIdentifier_primitive(
        self, ctx: VerseQLParser.Identifier_primitiveContext
    ):
        pass

    # Exit a parse tree produced by VerseQLParser#identifier_primitive.
    def exitIdentifier_primitive(
        self, ctx: VerseQLParser.Identifier_primitiveContext
    ):
        pass

    # Enter a parse tree produced by VerseQLParser#literal_null.
    def enterLiteral_null(self, ctx: VerseQLParser.Literal_nullContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_null.
    def exitLiteral_null(self, ctx: VerseQLParser.Literal_nullContext):
        ctx.value = None

    # Enter a parse tree produced by VerseQLParser#literal_true.
    def enterLiteral_true(self, ctx: VerseQLParser.Literal_trueContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_true.
    def exitLiteral_true(self, ctx: VerseQLParser.Literal_trueContext):
        ctx.value = True

    # Enter a parse tree produced by VerseQLParser#literal_false.
    def enterLiteral_false(self, ctx: VerseQLParser.Literal_falseContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_false.
    def exitLiteral_false(self, ctx: VerseQLParser.Literal_falseContext):
        ctx.value = False

    # Enter a parse tree produced by VerseQLParser#literal_string.
    def enterLiteral_string(self, ctx: VerseQLParser.Literal_stringContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_string.
    def exitLiteral_string(self, ctx: VerseQLParser.Literal_stringContext):
        ctx.value = ctx.getText()

    # Enter a parse tree produced by VerseQLParser#literal_integer.
    def enterLiteral_integer(self, ctx: VerseQLParser.Literal_integerContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_integer.
    def exitLiteral_integer(self, ctx: VerseQLParser.Literal_integerContext):
        ctx.value = int(ctx.getText())

    # Enter a parse tree produced by VerseQLParser#literal_decimal.
    def enterLiteral_decimal(self, ctx: VerseQLParser.Literal_decimalContext):
        pass

    # Exit a parse tree produced by VerseQLParser#literal_decimal.
    def exitLiteral_decimal(self, ctx: VerseQLParser.Literal_decimalContext):
        ctx.value = float(ctx.getText())


del VerseQLParser
