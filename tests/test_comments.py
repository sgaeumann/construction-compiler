# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

import io
import sys

from loguru import logger

from ebnf_compiler.parser import Parser
from ebnf_compiler.scanner import Scanner

SRC = """
(*
   outer comment = 1234abcdefg (*
   inner comment... !!$
*)
*)
syntax = {production}.
production = identifier "=" expression "." .
expression = term {"|" term}.
(* this is a comment
*) (*
   this is also a comment
*)
term = factor {factor}.
factor = identifier | string | "(" expression ")" | "[" expression "]" | "{" expression "}".
"""


def test_comments():
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    source = io.StringIO(SRC)
    scanner.init(source)
    parser = Parser(scanner=scanner, terminal_sym=set(), sym=set())

    parser.parse()
