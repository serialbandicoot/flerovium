from enum import Enum
from unittest import case


class Tag(Enum):

    A = "a"
    INPUT = "input"
    BUTTON = "button"
    DIV = "div"
    FORM = "form"


    @staticmethod
    def to_enum(enum: str):
        enum = enum.lower()
        if enum == "a":
            return Tag.A 
        elif enum == "input":
            return Tag.INPUT
        elif enum == "button":
            return Tag.BUTTON
        elif enum == "div":
            return Tag.DIV