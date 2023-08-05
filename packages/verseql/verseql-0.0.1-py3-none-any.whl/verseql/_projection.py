from __future__ import annotations

from typing import Any, Optional, Tuple

from ._expression import Expression


class Projection:
    def __init__(
        self,
        *args: ProjectionItem
        | str
        | Expression
        | Tuple[str | Expression, str],
        **kwargs: Any,
    ):
        if args:
            self._all = False
            self._items = []
            for item in args:
                if isinstance(item, ProjectionItem):
                    self._items.append(item)
                elif isinstance(item, (str, Expression)):
                    self._items.append(ProjectionItem(expr=item))
                elif isinstance(item, tuple):
                    self._items.append(
                        ProjectionItem(expr=item[0], as_identifier=item[1])
                    )
        else:
            self._all = True

    def __str__(self) -> str:
        if self._all:
            return "*"
        else:
            return ", ".join([str(i) for i in self._items])


class ProjectionItem:
    def __init__(
        self,
        expr: Expression | str,
        as_identifier: Optional[str] = None,
        **kwargs: Any,
    ):
        self._expr = expr
        self._as_identifier = as_identifier

    def __str__(self) -> str:
        _str = str(self._expr)
        if self._as_identifier:
            _str = f"{_str} AS {self._as_identifier}"
        return _str
