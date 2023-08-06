#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       test_try_parse.py
from unittest import TestCase

from crispy.crispy import Crispy


class Test_Try_Parse(TestCase):
    def test_try_parse_case1(self):
        expected = "string"
        actual = Crispy.try_parse("string", str)
        self.assertEqual(expected, actual)

    def test_try_parse_case2(self):
        expected = True
        actual = Crispy.try_parse("true", bool)
        self.assertEqual(expected, actual)

    def test_try_parse_case3(self):
        expected = False
        actual = Crispy.try_parse("false", bool)
        self.assertEqual(expected, actual)

    def test_try_parse_case4(self):
        expected = "false"
        actual = Crispy.try_parse("false", str)
        self.assertEqual(expected, actual)
