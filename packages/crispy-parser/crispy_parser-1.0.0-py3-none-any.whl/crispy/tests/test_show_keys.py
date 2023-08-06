#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       test_show_keys.py
from unittest import TestCase

from crispy.crispy import Crispy


class Test_Show_Keys(TestCase):
    def test_show_keys_case1(self):
        c = Crispy()
        c.add_variable("name", str)
        expected = "-n, --name: name\n"
        actual = c.show_keys()
        self.assertEqual(expected, actual)

    def test_show_keys_case2(self):
        c = Crispy(accept_shortform=False)
        c.add_variable("name", str)
        expected = "--name: name\n"
        actual = c.show_keys()
        self.assertEqual(expected, actual)

    def test_show_keys_case3(self):
        c = Crispy(accept_longform=False)
        c.add_variable("name", str)
        expected = "-n: name\n"
        actual = c.show_keys()
        self.assertEqual(expected, actual)
