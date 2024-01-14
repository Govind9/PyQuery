from typing import List
import pandas as pd
from lexicon import TYPE, load_keywords, load_operators


KEYWORDS = load_keywords()
OPERATORS = load_operators()

class Token:
    def __init__(self, token: str, token_type: TYPE = None) -> None:
        self.token = token.upper().strip()
        self.type = token_type
        if self.type is None:
            self.set_type()

    def __str__(self) -> str:
        return self.token
    
    def __len__(self) -> int:
        return len(self.token)
    
    def __eq__(self, t2) -> bool:
        return self.token == t2.token and self.type == t2.type
    
    def _is_keyword(self) -> bool:
        return self.token in KEYWORDS
    
    def _is_op(self) -> bool:
        return self.token in OPERATORS
    
    def _is_string(self) -> bool:
        return (
            self.token.startswith("'") and self.token.endswith("'")
            or self.token.startswith('"') and self.token.endswith('"')
        )

    def _is_int(self) -> bool:
        try:
            int(self.token)
            return True
        except:
            return False

    def _is_float(self) -> bool:
        try:
            float(self.token)
            return True
        except:
            return False

    def _is_value(self) -> bool:
        return self._is_string() or self._is_int() or self._is_float()
    
    def set_type(self):
        if self._is_keyword():
            self.type = TYPE.KEYWORD
        elif self._is_value():
            self.type = TYPE.VALUE
        elif self.token == ",":
            self.type = TYPE.COMMA
        elif self.token == ";":
            self.type = TYPE.SEMICOLON
        elif self._is_op():
            self.type = TYPE.OPERATOR
        else:
            self.type = TYPE.NAME
    
    def split(self, sep: str) -> List:
        return [Token(s) for s in self.token.split(sep)]


class Expression:
    def __init__(self, t1: Token, t2: Token, op: Token) -> None:
        self.t1 = t1
        self.t2 = t2
        self.op = op

    def __str__(self):
        return f"{self.t1} {self.op} {self.t2}"
    
    def apply(self, table: pd.DataFrame) -> pd.DataFrame:
        c1 = self.t1.token
        c2 = self.t2.token
        if self.t2._is_string():
            c2 = c2.strip('"').strip("'")
        op = self.op.token
        if op == "=":
            res = table[table[c1] == c2]
        elif op == ">":
            res = table[table[c1] > c2]
        elif op == "<":
            res = table[table[c1] < c2]
        elif op == "<=":
            res = table[table[c1] <= c2]
        elif op == ">=":
            res = table[table[c1] >= c2]
        elif op == "<>":
            res = table[table[c1] != c2]
        return res.reset_index(drop=True)

class Clause:
    def __init__(self):
        pass


def expected_next(token: Token) -> List:
    if token == Token("select"):
        return [(TYPE.NAME, 2)]
    elif token == Token("from"):
        return [(TYPE.NAME, 1)]
    elif token == Token("where"):
        return None
