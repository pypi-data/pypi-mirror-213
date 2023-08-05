from __future__ import annotations

from enum import Enum
from typing import Optional, Tuple

from ._expression import Expression


class Direction(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Order:
    def __init__(
        self, *args: OrderTerm | str | Tuple[str, Direction], **kwargs
    ):
        self._terms = []
        if args:
            for term in args:
                if isinstance(term, OrderTerm):
                    self._terms.append(term)
                elif isinstance(term, str):
                    self._terms.append(OrderTerm(expr=term))
                elif isinstance(term, tuple):
                    self._terms.append(
                        OrderTerm(expr=term[0], direction=term[1])
                    )
                else:
                    raise ValueError("Order term has invalid type")

    def __str__(self) -> str:
        if self._terms:
            return ", ".join([str(t) for t in self._terms])
        return ""


class OrderTerm:
    def __init__(
        self,
        expr: Expression | str,
        direction: Optional[Direction | str] = None,
        **kwargs,
    ):
        self._expr = expr
        if direction is None:
            self._direction = None
        elif isinstance(direction, Direction):
            self._direction = direction.value
        elif isinstance(direction, str):
            self._direction = direction.upper()
        else:
            raise ValueError("Order Direction has invalid type")

    def __str__(self) -> str:
        _str = str(self._expr)
        if self._direction:
            _str = f"{_str} {self._direction}"
        return _str
