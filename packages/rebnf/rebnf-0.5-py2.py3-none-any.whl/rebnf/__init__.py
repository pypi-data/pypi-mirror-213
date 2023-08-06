"""
ReBNF: Regexes for Extended Backus-Naur Form

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
from . import lexers
from . import parsers

assert all((lexers, parsers))

__author__ = "opsocket <opsocket@pm.me>"
__description__ = "Lexer and parser for the ReBNF metasyntax language"
__version__ = "0.5"
__ascii__ = """
ooooooooo.             oooooooooo.  ooooo      ooo oooooooooooo 
`888   `Y88.           `888'   `Y8b `888b.     `8' `888'     `8 
 888   .d88'  .ooooo.   888     888  8 `88b.    8   888         
 888ooo88P'  d88' `88b  888oooo888'  8   `88b.  8   888oooo8    
 888`88b.    888ooo888  888    `88b  8     `88b.8   888    "    
 888  `88b.  888    .o  888    .88P  8       `888   888         
o888o  o888o `Y8bod8P' o888bood8P'  o8o        `8  o888o       """

__doc__ = Rf"""

{__ascii__} v{__version__}

{__description__}

"""


def tokenize(code):
    """
    Tokenizes the provided rebnf code using the lexer.

    :param code: The rebnf code to tokenize.
    :type code: str

    :returns: A list of tokens representing the code.
    :rtype: list[str]
    """
    lexer = lexers.REBNFLexer()
    return lexer.tokenize(code)


def parse(code):
    raise NotImplementedError()
