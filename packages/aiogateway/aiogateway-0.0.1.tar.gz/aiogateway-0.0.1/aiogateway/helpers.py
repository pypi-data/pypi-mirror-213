import base64
import json
from datetime import date, datetime, time
from enum import Enum
from functools import singledispatch
from typing import Any, List, Union
from uuid import UUID

from aiohttp.web import Response
from pydantic import BaseModel  # pylint: disable=no-name-in-module


def jsonable_encoder(
    obj: Any,
    *,
    include: List[str] = [],
    exclude: List[str] = [],
    by_alias: bool = False,
    skip_defaults: bool = False,
    custom_encoder: Any = None,
) -> Any:
    """
    Convert any object to a JSON-serializable object.

    This function is used by Aiofauna to convert objects to JSON-serializable objects.

    It supports all the types supported by the standard json library, plus:

    * datetime.datetime
    * datetime.date
    * datetime.time
    * uuid.UUID
    * enum.Enum
    * pydantic.BaseModel
    """

    if obj is str:
        return "string"
    if obj is int or obj is float:
        return "integer"
    if obj is bool:
        return "boolean"
    if obj is None:
        return "null"
    if obj is list:
        return "array"
    if obj is dict:
        return "object"
    if obj is bytes:
        return "binary"
    if obj is datetime:
        return "date-time"
    if obj is date:
        return "date"
    if obj is time:
        return "time"
    if obj is UUID:
        return "uuid"
    if obj is Enum:
        return "enum"
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, dict):
        return {
            jsonable_encoder(
                k,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            ): jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for k, v in obj.items()
        }
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode()
    if isinstance(obj, (set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, UUID):
        return str(obj)
    return custom_encoder().default(obj)

@singledispatch
def do_response(response: Any) -> Response:
    """
    Flask-esque function to make a response from a function.
    """
    return response


@do_response.register(BaseModel)
def _(response: BaseModel) -> Response:
    return Response(
        status=200, body=response.json(
            exclude_none=True
            ), content_type="application/json"
    )


@do_response.register(dict)
def _(response: dict) -> Response:
    return Response(
        status=200, body=json.dumps(response), content_type="application/json"
    )


@do_response.register(str)
def _(response: str) -> Response:
    if "<html>" in response:
        return Response(status=200, text=response, content_type="text/html")
    return Response(status=200, text=response, content_type="text/plain")

@do_response.register(bytes)
def _(response: bytes) -> Response:
    return Response(status=200, body=response, content_type="application/octet-stream")


@do_response.register(int)
def _(response: int) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(float)
def _(response: float) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(bool)
def _(response: bool) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(list)
def _(response: List[Union[BaseModel, dict, str, int, float]]) -> Response:
    processed_response = []

    for item in response:
        if isinstance(item, BaseModel):
            processed_response.append(item.json(exclude_none=True))
        elif isinstance(item, dict):
            processed_response.append(item)
        elif isinstance(item, str):
            processed_response.append(item)
        elif isinstance(item, (int, float, bool)):
            processed_response.append(str(item))
        else:
            raise TypeError(f"Cannot serialize type {type(item)}")
    return Response(
        status=200, body=json.dumps(processed_response), content_type="application/json"
    )