"""
__main__.py - command-line interface

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
from . import tokenize, __ascii__, __version__
import argparse

__description__ = Rf"""

{__ascii__} v{__version__}

"""

def main():
    parser = argparse.ArgumentParser("tokenize", description=__description__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "filepath", type=str, help="filepath to read for tokenization"
    )
    parser.add_argument("-p", "--pretty", action='store_true', help="prints a pretty output")

    args = parser.parse_args()

    if args.filepath:
        with open(args.filepath, "r") as code:
            tokens = tokenize(code.read())
        if args.pretty:
            from pprint import pprint
            pprint(tokens)
        else:
            print(tokens)


if __name__ == "__main__":
    main()
