import unittest

from hamcrest import assert_that, has_entry, equal_to

from tests.core import HttpClient
from tests.given import given, when, then
from tests.steps import prepare_api_server, create_test_client


class TestHealth(unittest.TestCase):
    def test_when_get_request_sent_then_OK_response_returned(self):
        with given([
            prepare_api_server(),
            create_test_client(),
        ]) as context:
            client: HttpClient = context.client

            with when("Health GET request is sent"):
                response = client.get(
                    url="/api/v1/health"
                )

            with then("Status code OK is returned"):
                assert_that(response, has_entry("status", equal_to("OK")))
