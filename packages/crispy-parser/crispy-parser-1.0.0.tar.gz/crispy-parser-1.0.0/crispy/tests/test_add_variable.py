#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       test_add_variable.py
from unittest import TestCase

from crispy.crispy import Crispy
from crispy.duplicate_name_exception import DuplicateNameException


class Test_Add_Variable(TestCase):
    def setUp(self) -> None:
        self.c = Crispy()
        self.c.add_variable("name", str)
        self.c.add_variable("age", int)
        self.c.add_variable("addr", str)

    def test_add_variable_with_unique_name(self):
        self.assertEqual(self.c.variables["name"], str)
        self.assertEqual(self.c.accepted_keys["--name"], "name")

    def test_add_variable_with_duplicate_name(self):
        with self.assertRaises(DuplicateNameException):
            self.c.add_variable("name", str)

    def test_add_variable_with_unique_shortform(self):
        self.assertEqual(self.c.variables["name"], str)
        self.assertEqual(self.c.accepted_keys["-n"], "name")

    def test_add_variable_with_duplicate_shortform(self):
        expected = {"-A": "addr", "--addr": "addr", "-a": "age", "--age": "age", "-n": "name", "--name": "name"}
        self.assertEqual(expected, self.c.accepted_keys)

    def test_add_variable_without_accepting_shortform(self):
        self.c = Crispy(accept_shortform=False)
        self.c.add_variable("name", str)
        self.assertDictEqual(self.c.accepted_keys, {"--name": "name"})

    def test_add_variable_without_accepting_longform(self):
        self.c = Crispy(accept_longform=False)
        self.c.add_variable("name", str)
        self.assertDictEqual(self.c.accepted_keys, {"-n": "name"})
