# ReBNF

<div>
  <a href="#"><img src="https://img.shields.io/badge/%F0%9F%94%96%20Version-0.6-ec3832.svg?color=ec3832&style=flat"/></a>
  <a href="https://opsocket.com" style="text-decoration: none;">
    <img alt="opsocket" height="42" src="https://gitlab.com/opsocket/rebnf/-/raw/main/docs/assets/imgs/logo.svg" loading="lazy" />
  </a>
</div>


**ReBNF** (*Regexes for Extended Backus-Naur Form*) is a notation used to define the
syntax of a language using regular expressions.

It is an extension of the EBNF (Extended Backus-Naur Form) notation, allowing
for more flexibility and ease of use.

```
ooooooooo.             oooooooooo.  ooooo      ooo oooooooooooo 
`888   `Y88.           `888'   `Y8b `888b.     `8' `888'     `8 
 888   .d88'  .ooooo.   888     888  8 `88b.    8   888         
 888ooo88P'  d88' `88b  888oooo888'  8   `88b.  8   888oooo8    
 888`88b.    888ooo888  888    `88b  8     `88b.8   888    "    
 888  `88b.  888    .o  888    .88P  8       `888   888         
o888o  o888o `Y8bod8P' o888bood8P'  o8o        `8  o888o       
```

## Table of Contents

- [Syntax](#syntax)
- [Example](#example)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Syntax

The **ReBNF** notation uses regular expressions to define the structure of a
language. Each *rule* consists of a *left-hand side* (non-terminal) and a
*right-hand side* separated by an **assignment operator** (either `::=`, `:=` or `=`).

The general syntax of a **ReBNF** rule is as follows:

```
<alnum> ::= r"[a-zA-Z0-9]" ; # any alphanumeric characters
```

## Example

Here's a short example of a **ReBNF** definition for a simple arithmetic expression language:

```
expression = term { ('+' | '-') term }
term = factor { ('*' | '/') factor }
factor = number | expression
number = r'\d+'
```
## Usage

**ReBNF** notation is used to define the syntax of programming languages,
  configuration file formats, or any other formal language. 

It provides a concise and powerful way to express language structures with
a addition of regular expressions.

> Note that the functions in this module are only designed to parse
syntactically valid **ReBNF** code (code that does not raise when parsed using
`parse()`). The behavior of the functions in this module is undefined when
providing invalid **ReBNF** code and it can change at any point. 

## Contributing

Contributions are welcome! If you have suggestions, improvements, or new ideas
related to the **ReBNF** notation, please feel free to open an issue or submit a
pull request.

## License

This project is licensed under the [GPLv3][#gplv3] license - see [LICENSE.md][#license] for details..

[#gplv3]: https://www.gnu.org/licenses/gpl-3.0.html
[#license]: https://gitlab.com/opsocket/rebnf/-/blob/main/LICENSE.md
