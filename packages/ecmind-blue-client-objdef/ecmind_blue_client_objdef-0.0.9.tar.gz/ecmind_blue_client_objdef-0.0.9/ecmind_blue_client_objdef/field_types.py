from enum import Enum

class FieldTypes(Enum):
    INTEGER = '9'
    PAGECONTROL = 'C'
    STRING = 'X'
    STRING_UPPER = 'G'
    RIGHTGROUP = 'R'
    TABLE = 'W'
    WEB = 'E'
    BUTTON = 'K'
    DATE = 'D'
    DOUBLE = '#'
    RADIO = '1'
    CHECKBOX = '0'
    YES_NO = 'Q'
    LETTERS_ONLY = 'A'
    ALPHA_DIGITS = 'Z'

