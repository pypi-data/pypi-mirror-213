#
#       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
#       crispy                  2023
#
#       duplicate_name_exception.py


class DuplicateNameException(Exception):
    def __init__(self, message):
        self.message = message
