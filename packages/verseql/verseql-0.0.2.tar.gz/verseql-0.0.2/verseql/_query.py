from typing import Optional

from ._expression import Expression, PrimtiveType
from ._order import Order
from ._projection import Projection


class Query:
    def __init__(
        self,
        projection: Optional[Projection] = None,
        filter: Optional[Expression] = None,
        order: Optional[Order] = None,
        limit: Optional[Expression | PrimtiveType] = None,
        offset: Optional[Expression | PrimtiveType] = None,
        store: str = "$store",
        **kwargs,
    ):
        self._projection = (
            projection if projection is not None else Projection()
        )
        self._filter = filter
        self._order = order

        if limit is not None:
            self._limit = Expression._normalize(expr=limit)
        else:
            self._limit = limit

        if offset is not None:
            self._offset = Expression._normalize(expr=offset)
        else:
            self._offset = offset

        if store is not None:
            self._store = store
        else:
            raise ValueError("Store name has invalid data")

    def __str__(self) -> str:
        _str = f"SELECT {str(self._projection)} FROM {self._store}"
        if self._filter is not None:
            _str = _str + f" WHERE {str(self._filter)}"
        if self._order is not None:
            _str = _str + f" ORDER BY {str(self._order)}"
        if self._limit is not None:
            _str = _str + f" LIMIT {str(self._limit)}"
        if self._offset is not None:
            _str = _str + f" OFFSET {str(self._offset)}"
        return _str
