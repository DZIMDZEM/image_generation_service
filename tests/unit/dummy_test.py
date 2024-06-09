import unittest

from hamcrest import is_, assert_that, equal_to

from tests.given import given, when, then


class DummyTest(unittest.TestCase):
    def test_dummy(self):
        with given():
            pass

        with when():
            pass

        with then():
            assert_that(1, is_(equal_to(1)))
