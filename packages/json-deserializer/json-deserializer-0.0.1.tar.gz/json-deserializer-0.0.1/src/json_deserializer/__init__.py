from decimal import Decimal
from typing import (
    Sequence,
    Mapping,
    Any,
    Callable
)


def deserialize(data: Any) -> Any:
    """
    For objects that are `almost` a duck, but not quite
    This keeps json decoder from blowing up
    """
    if isinstance(data, Mapping) and not isinstance(data, dict):
        data = dict(data)
        res = deserialize(data)
    elif isinstance(data, Sequence) and not isinstance(data, str):
        res = []
        for x in data:
            res.append(deserialize(x))
    elif isinstance(data, dict):
        res = {}
        for k, v in data.items():
            res[k] = deserialize(v)
    elif isinstance(data, Callable):
        res = str(data)
    elif isinstance(data, Decimal):
        res = float(data)
    else:
        res = data

    return res
