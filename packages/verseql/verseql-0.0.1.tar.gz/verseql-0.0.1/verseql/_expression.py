from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Any, Tuple, TypeAlias

PrimtiveType: TypeAlias = str | int | float | bool | None


class Expression(ABC):
    @staticmethod
    def _normalize(expr: Expression | PrimtiveType):
        if expr is None or isinstance(expr, (str, int, float, bool)):
            return Primitive(expr=expr)
        elif isinstance(expr, Expression):
            return expr
        else:
            ValueError("Expression has invalid type")


class Primitive(Expression):
    def __init__(self, expr: PrimtiveType, **kwargs: Any):
        self._expr = expr

    def __str__(self) -> str:
        if self._expr is None:
            return "NULL"
        elif isinstance(self._expr, bool):
            return str(self._expr).upper()
        elif isinstance(self._expr, (str, int, float)):
            return str(self._expr)
        else:
            raise ValueError("Primitive expression has invalid type")


class Function(Expression):
    def __init__(self, name: FunctionName | str, *args: Any, **kwargs: Any):
        self._name = name
        self._args = tuple(Expression._normalize(a) for a in args)

    def __str__(self) -> str:
        _str = None
        if isinstance(self._name, FunctionName):
            _str = self._name.value
        elif isinstance(self._name, str):
            _str = self._name.upper()
        else:
            raise ValueError("Function name has invalid type")
        _str = _str + f"({', '.join(str(a) for a in self._args)})"
        return _str


class Predicate(Expression):
    def __init__(
        self,
        left_expr: Expression | PrimtiveType,
        op: PredicateOp | str,
        right_expr: Expression
        | PrimtiveType
        | Tuple[Expression | PrimtiveType, ...],
        **kwargs: Any,
    ):
        self._left_expr = Expression._normalize(expr=left_expr)
        if isinstance(right_expr, tuple):
            self._right_expr = tuple(
                Expression._normalize(t) for t in right_expr
            )
        else:
            self._right_expr = Expression._normalize(expr=right_expr)

        if isinstance(op, PredicateOp):
            self._op = op.value
        elif isinstance(op, str):
            self._op = op.upper()
        else:
            ValueError("Op has invalid type")

    def __str__(self) -> str:
        _str = f"{str(self._left_expr)} {self._op} "
        if self._op == PredicateOp.BETWEEN:
            _str = (
                _str
                + f"{str(self._right_expr[0])} AND {str(self._right_expr[1])}"
            )
        elif isinstance(self._right_expr, tuple):
            _str = _str + f"({', '.join(str(t) for t in self._right_expr)})"

        else:
            _str = _str + str(self._right_expr)
        return _str


class And(Expression):
    def __init__(
        self,
        left_expr: Expression | PrimtiveType,
        right_expr: Expression | PrimtiveType,
        **kwargs: Any,
    ):
        self._left_expr = Expression._normalize(left_expr)
        self._right_expr = Expression._normalize(right_expr)

    def __str__(self) -> str:
        return f"({str(self._left_expr)} AND {str(self._right_expr)})"


class Or(Expression):
    def __init__(
        self,
        left_expr: Expression | PrimtiveType,
        right_expr: Expression | PrimtiveType,
        **kwargs: Any,
    ):
        self._left_expr = Expression._normalize(left_expr)
        self._right_expr = Expression._normalize(right_expr)

    def __str__(self) -> str:
        return f"({str(self._left_expr)} OR {str(self._right_expr)})"


class Not(Expression):
    def __init__(self, expr: Expression | PrimtiveType, **kwargs: Any):
        self._expr = Expression._normalize(expr)

    def __str__(self) -> str:
        return f"NOT {str(self._expr)}"


class FunctionName(str, Enum):
    """Type Functions"""

    IS_TYPE = "IS_TYPE"
    IS_DEFINED = "IS_DEFINED"

    """Array Functions"""
    ARRAY_CONTAINS = "ARRAY_CONTAINS"
    ARRAY_LENGTH = "ARRAY_LENGTH"

    """String Functions"""
    CONTAINS = "CONTAINS"
    LENGTH = "LENGTH"
    STARTSWITH = "STARTSWITH"
    ENDSWITH = "ENDSWITH"

    """Aggregate Functions"""
    COUNT = "COUNT"


class PredicateOp(str, Enum):
    LT = "<"
    LT_EQ = "<="
    GT = ">"
    GT_EQ = ">="
    EQ = "="
    NEQ = "!="
    IN = "IN"
    NOT_IN = "NOT IN"
    BETWEEN = "BETWEEN"
