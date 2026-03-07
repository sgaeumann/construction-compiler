# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

import io
import sys

from loguru import logger

from ebnf_compiler.parser import Parser
from ebnf_compiler.scanner import Scanner

SRC = """
ident = letter { letter | digit }.
number = digit { digit }.
digit = "0" | "1" | "2" | "3".
"""


def test_ast_set():
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    source = io.StringIO(SRC)
    scanner.init(source)
    parser = Parser(scanner=scanner, terminal_sym=set(), sym=set())

    parser.parse()

    expected_terminal_sym = {"letter","digit"}
    expected_sym = {"Term","Expression","Production","Syntax"}

    assert(parser.terminal_sym == expected_terminal_sym)
    assert(parser.sym == expected_sym)