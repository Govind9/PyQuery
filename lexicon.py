from enum import Enum


def load_keywords():
    KEYWORDS = []
    try:
        with open("keywords.txt") as f:
            KEYWORDS = f.read().splitlines()
    except Exception as e:
        raise e
    KEYWORDS = [k.upper() for k in KEYWORDS]
    KEYWORDS = set(KEYWORDS)
    return KEYWORDS


def load_operators():
    OPERATORS = []
    try:
        with open("operators.txt") as f:
            OPERATORS = f.read().splitlines()
    except Exception:
        pass
    OPERATORS = set(OPERATORS)
    return OPERATORS


class TYPE(Enum):
    KEYWORD = "keyword"
    NAME = "name"
    VALUE = "value"
    COMMA = "comma"
    SEMICOLON = "semicolon"
    OPERATOR = "operator"
    EXPRESSION = "expression"
    OTHER = "other"
