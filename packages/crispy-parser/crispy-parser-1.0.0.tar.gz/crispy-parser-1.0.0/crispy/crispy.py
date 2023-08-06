#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       crispy.py
from typing import List, Dict, Type

from crispy.duplicate_name_exception import DuplicateNameException
from crispy.missing_value_exception import MissingValueException
from crispy.no_arguments_exception import NoArgumentsException
from crispy.unexpected_argument_exception import UnexpectedArgumentException


class Crispy:
    def __init__(self, accept_shortform=True, accept_longform=True):
        self.accepted_keys: Dict[str, str] = {}
        self.variables: Dict[str, Type[str | bool | int | float]] = {}

        if not (accept_shortform or accept_longform):
            raise ValueError("crispy: At least one form must be accepted!")
        self.accept_shortform = accept_shortform
        self.accept_longform = accept_longform

    def add_variable(self, name: str, var_type: Type[str | bool | int | float]):
        if name in self.variables:
            raise DuplicateNameException(f"crispy: variable with name '{name}' is present! Choose something else.")
        if self.accept_shortform:
            short_lower = f"-{name[0].lower()}"
            short_upper = f"-{name[0].upper()}"
            if short_lower not in self.accepted_keys:
                self.variables[name] = var_type
                self.accepted_keys[short_lower] = name
            elif short_upper not in self.accepted_keys:
                self.variables[name] = var_type
                self.accepted_keys[short_upper] = name
            else:
                raise ValueError(f"crispy: cannot add variable due to unavailable shortform!'-{short_lower}' "
                                 f"and '-{short_upper}' is reserved for other variables.")
        if self.accept_longform:
            self.variables[name] = var_type
            self.accepted_keys[f"--{name}"] = name

    def show_keys(self) -> str:
        keys: List[str] = list(self.accepted_keys.keys())
        twice = self.accept_shortform and self.accept_longform
        i = 0
        text = ""
        move = 2 if twice else 1

        while i < len(keys):
            name = self.accepted_keys[keys[i]]
            text += f"{keys[i]}, {keys[i + 1]}: {name}\n" if twice else f"{keys[i]}: {name}\n"
            i += move
        return text

    def parse_arguments(self, args: List[str]) -> Dict[str, str]:
        if not args:
            raise NoArgumentsException("crispy: no argument was given!")

        result = {}
        i, len_args = 0, len(args)
        while i < len_args:
            key = args[i]

            if key.strip() == "":
                i += 1
                continue

            if "=" not in key:
                if (i + 1 < len_args) and (args[i + 1] not in self.accepted_keys) and ("=" not in args[i + 1]):
                    value = args[i + 1]
                    i += 2
                else:
                    expected_type = self.variables.get(self.accepted_keys.get(key))
                    if expected_type == bool:
                        value = "True"
                        i += 1
                    else:
                        raise MissingValueException(f"crispy: missing value for variable '{self.accepted_keys[key]}'!")
            else:
                key, value = key.split("=", 1)
                i += 1

            accepted_key = self.accepted_keys.get(key)
            if accepted_key:
                result[accepted_key] = self.try_parse(value, self.variables.get(accepted_key))
            else:
                raise UnexpectedArgumentException(f"crispy: unexpected argument: '{key}'")

        for key, value in self.variables.items():
            if value == bool and key not in result:
                result[key] = False

        return result

    def parse_string(self, string: str, seperator=" ") -> dict:
        tokens: List[str] = str.split(string, seperator)
        return self.parse_arguments(tokens)

    @staticmethod
    def try_parse(value: str, expected_type: type) -> str | bool | int | float:
        if expected_type == bool:
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
        if expected_type == int:
            return int(value)
        if expected_type == float:
            return float(value)
        return value
