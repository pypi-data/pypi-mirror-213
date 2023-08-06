"""
lexers.py - lexer for the rebnf language

Copyright (C) 2023 opsocket <opsocket@pm.me>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from ply import lex


class Token(lex.LexToken):
    """
    This class describes a simple token wrapper.
    """

    def __init__(self, token):
        assert isinstance(token, lex.LexToken)
        super().__init__()
        self.__dict__.update(token.__dict__)

    def __str__(self):
        return super().__str__()[3:]
      

class REBNFLexer(object):
    tokens = (
        "REGEX",
        "IDENTIFIER",
        "ASSIGN",
        "GROUP_BEGIN",
        "GROUP_END",
        "OPTIONAL_BEGIN",
        "OPTIONAL_END",
        "REPETITION_BEGIN",
        "REPETITION_END",
        "SINGLE_QUOTE_STRING",
        "DOUBLE_QUOTE_STRING",
        "TERMINATOR",
        "OPTIONAL_OP",
        "ONE_OR_MORE_OP",
        "ZERO_OR_MORE_OP",
        "EXCEPT",
        "CONCAT",
        "ALTERNATE",
        "COMMENT_SINGLE",
        "COMMENT_MULTI",
    )

    t_ASSIGN = r"=|:=|::="
    t_GROUP_BEGIN = r"\("
    t_GROUP_END = r"\)"
    t_OPTIONAL_BEGIN = r"\["
    t_OPTIONAL_END = r"\]"
    t_REPETITION_BEGIN = r"{"
    t_REPETITION_END = r"}"
    t_TERMINATOR = r";|\."
    t_OPTIONAL_OP = r"\?"
    t_ONE_OR_MORE_OP = r"\+"
    t_ZERO_OR_MORE_OP = r"\*"
    t_EXCEPT = r"-"
    t_CONCAT = r","
    t_ALTERNATE = r"\|"
    t_COMMENT_SINGLE = r"\#.*"
    t_ignore = " \t\r\f\b"

    def t_REGEX(self, t):
        r"r(\'(\\.|[^\\\'])*\'|\"(\\.|[^\\\"])*\")"
        return t

    def t_IDENTIFIER(self, t):
        r"<[a-zA-Z][a-zA-Z0-9_]*>|[a-zA-Z][a-zA-Z0-9_]*"
        # support for optional identifier enclosures
        if t.value.startswith("<") and t.value.endswith(">"):
            t.value = t.value[1:-1]
        return t

    def t_COMMENT_MULTI(self, t):
        r"\(\*(?:.|\n)*\*\)"
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_SINGLE_QUOTE_STRING(self, t):
        r"\'(\\.|[^\\\'])*\'"
        t.value = t.value[1:-1]
        return t

    def t_DOUBLE_QUOTE_STRING(self, t):
        r"\"(\\.|[^\\\"])*\" "
        t.value = t.value[1:-1]
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_SYMBOL(self, t):
        r"<|>|-|\n|\t|\r|\f|\b"
        return t

    def t_error(self, t):
        print(f"\033[91millegal character: {t.value[0]}\033[0m")
        t.lexer.skip(1)

    def __init__(self):
        # build lexer
        self.lexer = lex.lex(module=self)

    def token(self):
        return self.lexer.token()

    def tokenize(self, code):
        self.lexer.input(code)
        output = []
        while token := self.lexer.token():
            tok = Token(token)
            output.append(tok)
        return output
