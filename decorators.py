from types import FunctionType
from typing import Any, Callable, TypeVar, cast
from functools import wraps
from flask.globals import request
from flask.json import jsonify

FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def json_only(func: FuncT) -> FuncT:
    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if not request.json:
            return (
                jsonify(
                    {"msg": "This endpoint only accept application/json content type"}
                ),
                401,
            )
        return func(*args, **kwargs)

    return cast(FuncT, wrapped)
