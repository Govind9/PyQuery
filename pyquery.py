from typing import Dict, Tuple, List
import pandas as pd
from lexicon import TYPE
from logic import Token, Expression
from exceptions import UnexpectedTokenError, ExecutionError


class DataBase:
    def __init__(
        self,
        database: Dict[str, pd.DataFrame],  
    ) -> None:
        self.db = {}
        self.add_database(database)

    def __str__(self) -> str:
        return self.query if self.query is not None else ""
    
    def add_database(self, database: Dict[str, pd.DataFrame]) -> None:
        self.db = {n.upper(): d for n, d in database.items()}
        for name, table in self.db.items():
            cols = table.columns
            cols = {c: c.upper() for c in cols}
            self.db[name] = table.rename(columns=cols)

    def add_table(
        self,
        table_name: str,
        table: pd.DataFrame
    ) -> None:
        self.db[table_name.upper()] = table

    def _split(tokens: List[Token], sep: str) -> List[str]:
        ret_tokens = []
        for token in tokens:
            new_tokens = token.split(sep)
            ret_tokens.extend([t for t in new_tokens if len(t) > 0])
        return ret_tokens
    
    def _tokenize(query: str) -> List[Token]:
        init_token = Token(query, TYPE.OTHER)
        tokens = [init_token]
        seps = [" ", ",", ";", "\n", "\t"]
        for sep in seps:
            tokens = DataBase._split(tokens, sep)
        return tokens

    def parse(self, query: str) -> Dict:
        tokens = DataBase._tokenize(query)
        actions = {
            "select_names": [],
            "table_name": None,
            "where_expressions": []
        }

        try:
            # query must start with select clause
            assert len(tokens) > 0
            assert tokens[0] == Token("select")
            # start getting column names till from clause
            for idx, token in enumerate(tokens):
                if idx == 0:
                    continue
                if token == Token("from"):
                    break
                if token.type != TYPE.NAME:
                    raise UnexpectedTokenError(token, TYPE.NAME)
                actions["select_names"].append(token.token)
            # after select, there must be a from
            assert tokens[idx] == Token("from")
            # get the table name
            idx += 1
            assert tokens[idx].type == TYPE.NAME
            actions["table_name"] = tokens[idx].token
            idx += 1
            expresions = []
            if idx < len(tokens):
                assert tokens[idx] == Token("where")
                assert idx + 4 == len(tokens)
                assert tokens[idx + 1].type == TYPE.NAME
                assert tokens[idx + 2].type == TYPE.OPERATOR
                assert tokens[idx + 3].type == TYPE.VALUE
                actions["where_expressions"].append(
                    Expression(
                        t1=tokens[idx + 1],
                        op=tokens[idx + 2],
                        t2=tokens[idx + 3]
                    )
                )
        except Exception as err:
            raise UnexpectedTokenError(err)

        return actions     

    def execute(self, actions: Dict) -> pd.DataFrame:
        try:
            cols = actions["select_names"]
            table_name = actions["table_name"]
            exps = actions["where_expressions"]
            assert table_name in self.db
            table = self.db[table_name]
            for col in cols:
                assert col in table.columns
            res = table
            for exp in exps:
                res = exp.apply(res)
            return res[cols].copy()
        except Exception as err:
            raise ExecutionError(err)
        
    def run(self, query: str) -> pd.DataFrame:
        actions = self.parse(query)
        return self.execute(actions)
