#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       test_parse_string.py
from unittest import TestCase

from crispy.crispy import Crispy


class Test_Parse_String(TestCase):
    def test_parse_string_case1(self):
        c = Crispy()
        c.add_variable("name", str)
        c.add_variable("age", int)
        c.add_variable("sex", bool)
        expected = {"sex": True, "name": "John", "age": 14}
        actual = c.parse_string("-s -n=John -a 14")
        self.assertEqual(expected, actual)
