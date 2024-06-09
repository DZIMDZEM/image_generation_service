from base64 import b64encode
from typing import List

from cattr import Converter
from flask.testing import FlaskClient

from src.api.core_features.infrastructure.json import create_rest_converter, from_json, to_json
from src.api.logger import get_logger

logger = get_logger(__name__)


def conditional_decorator(dec, condition):
    def decorator(func):
        if condition:
            return dec(func)
        else:
            return func

    return decorator


def client_from_json(response):
    data = response.data
    return from_json(data)


def raise_error(json):
    if json and "error" in json:
        raise Exception(json["message"])


class HttpClient:
    def __init__(self, app, credentials=None):
        self.app = app
        self.inner_client: FlaskClient = app.test_client()
        self.response = None
        self.credentials = credentials
        self.converter: Converter = create_rest_converter()

    def put(self, url, data, return_type=None, return_response=False):
        return self.request(url, method="PUT", data=data, return_type=return_type, return_response=return_response)

    def post(self, url, data, return_type=None, return_response=False, content_type="application/vnd.lucid+json"):
        return self.request(url, method="POST", data=data, return_type=return_type, return_response=return_response,
                            content_type=content_type)

    def get(self, url, return_type=None, return_response=False):
        return self.request(url, method="GET", return_type=return_type, return_response=return_response)

    def request(self, url, method, data=None, return_type=None, return_response=False,
                content_type="application/vnd.synth+json"):
        headers = self._create_auth()

        if data and "json" in content_type:
            data = self.converter.unstructure(data)
            data = to_json(data)

            logger.info("Request to %s %s %s", method, url, data)

        args = [url]

        kw = dict(
            method=method,
            data=data,
            content_type=content_type,
            headers=headers,
        )

        response = self.inner_client.open(
            *args, **kw,
        )

        if return_response:
            return response

        self.response = response

        if response.status_code >= 400:
            raise Exception(response.data)

        if response.content_type not in ["application/json", "application/vnd.lucid+json"]:
            return response

        json = client_from_json(response)
        raise_error(json)

        if json and return_type:
            if isinstance(json, list):
                json = self.converter.structure(json, List[return_type])
            else:
                json = self.converter.structure(json, return_type)

        return json

    def _create_auth(self):
        if not self.credentials:
            return {}

        credentials = self.credentials

        basic_token = b64encode("{}:{}".format(credentials[0], credentials[1]).encode("ascii")).decode("ascii")

        return {
            "Authorization": "Basic %s" % basic_token,
        }

    def delete(self, url, return_type=None, return_response=True):
        return self.request(url, method="DELETE", return_type=return_type, return_response=return_response)
