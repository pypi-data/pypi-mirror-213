"""
parsers.py - parser for the rebnf language

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
from ply import yacc
from . import lexers


class REBNFParser(object):
    """
    This class describes a rebnf parser.
    """

    tokens = lexers.REBNFLexer.tokens

    def __init__(self):
        self.lexer = lexers.REBNFLexer()
        self.parser = yacc.yacc(module=self)

    def p_grammar(self, p):
        """
        grammar : comment grammar
                | rule grammar
                | comment
                | rule
        """
        print(list(p))
        # if len(self, p) == 3:
        #     p[0] = ('GRAMMAR', p[1])
        # elif len(self, p) == 2:
        #     print('here', list(self, p))
        #     p[0] = p[1]

    def p_comment(self, p):
        """comment : COMMENT_SINGLE
        | COMMENT_MULTI
        """
        p[0] = ("COMMENT", p[1])

    def p_rule(self, p):
        """rule : lhs ASSIGN rhs TERMINATOR"""
        p[0] = ("RULE", (p[1], p[3]))

    def p_lhs(self, p):
        """lhs : IDENTIFIER"""
        p[0] = p[1]

    def p_rhs(self, p):
        """rhs : alternation"""
        p[0] = p[1]

    def p_alternation(self, p):
        """
        alternation : concatenation ALTERNATE alternation
                    | concatenation
        """
        if len(self, p) == 4:
            p[0] = ("ALTERNATION", (p[1], p[3]))
        else:
            p[0] = p[1]

    def p_concatenation(self, p):
        """
        concatenation : factor CONCAT concatenation
                      | factor
        """
        if len(self, p) == 4:
            p[0] = ("CONCAT", (p[1], p[2]))
        else:
            p[0] = p[1]

    def p_factor(self, p):
        """
        factor : term OPTIONAL_OP
               | term ZERO_OR_MORE_OP
               | term ONE_OR_MORE_OP
               | term EXCEPT term
               | term
        """
        if len(self, p) == 3:
            if p[2] == "?*+":
                p[0] = (p[2], p[1])
        elif len(self, p) == 4:
            p[0] = ("EXCEPT", (p[1], p[2]))
        elif len(self, p) == 2:
            p[0] = p[1]

    def p_term(self, p):
        """
        term : GROUP_BEGIN rhs GROUP_END
             | OPTIONAL_BEGIN rhs OPTIONAL_END
             | REPETITION_BEGIN rhs REPETITION_END
             | regex
             | terminal
             | identifier
        """
        if len(self, p) == 4:
            if p[1] == "(":
                p[0] = ("GROUP", p[2])
            if p[1] == "[":
                p[0] = ("OPTIONAL", p[2])
            if p[1] == "{":
                p[0] = ("REPETITION", p[2])
        elif len(self, p) == 2:
            p[0] = p[1]

    def p_term_regex(self, p):
        """regex : REGEX"""
        p[0] = ("REGEX", p[1])

    def p_terminal(self, p):
        """
        terminal : single_quote_string
                 | double_quote_string
        """
        p[0] = ("STRING", p[1])

    def p_single_quote_string(self, p):
        """single_quote_string : SINGLE_QUOTE_STRING"""
        p[0] = ("SINGLE", p[1])

    def p_double_quote_string(self, p):
        """double_quote_string : DOUBLE_QUOTE_STRING"""
        p[0] = ("DOUBLE", p[1])

    def p_identifier(self, p):
        """identifier : IDENTIFIER"""
        p[0] = ("IDENTIFIER", p[1])

    def find_column(self, input, token):
        line_start = input.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def p_error(self, t):
        if t is not None:
            print(
                f"syntax error at line {t.lineno}, column {self.find_column(t.lexer.lexdata, t)}: unexpected token '{t.value}'"
            )
        return t
