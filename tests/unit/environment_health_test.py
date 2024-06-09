import unittest

from hamcrest import assert_that, greater_than_or_equal_to
from tests.given import given, when, then


class EnvironmentHealthTest(unittest.TestCase):
    def test_environment_has_numpy_more_or_equal_to_1_21_0(self):
        with given():
            pass

        with when():
            import numpy

        with then():
            assert_that(numpy.__version__, greater_than_or_equal_to('1.26.4'))
