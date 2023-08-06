#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       missing_value_exception.py


class MissingValueException(Exception):
    def __init__(self, message):
        self.message = message
