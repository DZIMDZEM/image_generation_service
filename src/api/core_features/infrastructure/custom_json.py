import datetime
import json
from base64 import b64encode, b64decode
from decimal import Decimal
from typing import TypeVar

from bson import ObjectId
from cattr import Converter
from dateutil.parser import parse
from flask import current_app, make_response
from injector import singleton, provider, Module


def get_class(kls):
    parts = kls.split(".")
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def fullname(o):
    return o.__module__ + "." + o.__class__.__qualname__


def json_converter(o):
    if isinstance(o, datetime.datetime):
        return str(o.isoformat())
    if isinstance(o, Decimal):
        return int(o)


def from_json(data):
    return json.loads(data)


def to_json(dict_o):
    return json.dumps(dict_o, default=json_converter)


def object_id_to_str(data):
    if not data:
        return None
    return str(data)


def str_to_object_id(data, obj_type):
    if not data:
        return None
    return ObjectId(data)


def bytes_to_str(data):
    if not data:
        return None
    res = b64encode(data).decode("ascii")
    return res


def str_to_bytes(data, obj_type):
    if not data:
        return None
    res = b64decode(data.encode("ascii"))
    return res


def type_to_str(data: type):
    if not data:
        return None
    return fullname(data)


def str_to_type(data: str, obj_type):
    if not data:
        return None
    return get_class(data)


def string_to_datetime(data, obj_type):
    if not data:
        return None
    return parse(data)


def string_to_date(data, obj_type):
    if not data:
        return None
    return parse(data).date()


def date_to_string(data):
    if not data:
        return None
    return data.isoformat()


RestConverter = TypeVar("RestConverter")


def create_rest_converter():
    atc = Converter()

    atc.register_structure_hook(dict, lambda c, t: c)
    atc.register_unstructure_hook(dict, lambda c: c)

    atc.register_structure_hook(bytes, str_to_bytes)
    atc.register_unstructure_hook(bytes, bytes_to_str)

    atc.register_structure_hook(ObjectId, str_to_object_id)
    atc.register_unstructure_hook(ObjectId, object_id_to_str)

    atc.register_structure_hook(type, str_to_type)
    atc.register_unstructure_hook(type, type_to_str)

    atc.register_unstructure_hook(datetime.datetime, date_to_string)
    atc.register_structure_hook(datetime.datetime, string_to_datetime)

    atc.register_unstructure_hook(datetime.date, date_to_string)
    atc.register_structure_hook(datetime.date, string_to_date)

    return atc


class JsonModule(Module):
    @singleton
    @provider
    def provide_rest_converter(self, ) -> RestConverter:
        return create_rest_converter()


rest_converter = create_rest_converter()


def output_vnd_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    settings = current_app.config.get("RESTFUL_JSON", {})

    # If we"re in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won"t override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault("indent", 4)
    data = rest_converter.unstructure(data)
    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = json.dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
