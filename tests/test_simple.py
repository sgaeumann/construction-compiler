import io
import sys

from loguru import logger

from ebnf_compiler.parser import Parser
from ebnf_compiler.scanner import Scanner

SRC = """
syntax = {production}.
production = identifier "=" expression "." .
expression = term {"|" term}.
term = factor {factor}.
factor = identifier | string | "(" expression ")" | "[" expression "]" | "{" expression "}".
"""


def test_simple():
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    source = io.StringIO(SRC)
    scanner.init(source)
    parser = Parser(scanner=scanner)

    parser.parse()