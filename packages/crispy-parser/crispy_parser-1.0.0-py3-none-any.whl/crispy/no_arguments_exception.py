#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       no_arguments_exception.py


class NoArgumentsException(Exception):
    def __init__(self, message):
        self.message = message
