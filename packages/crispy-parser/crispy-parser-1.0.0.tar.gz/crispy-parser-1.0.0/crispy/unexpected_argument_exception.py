#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       unexpected_argument_exception.py


class UnexpectedArgumentException(Exception):
    def __init__(self, message):
        self.message = message
