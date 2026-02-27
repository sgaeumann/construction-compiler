# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Compiler
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from rich.console import Console

from .parser import Parser
from .scanner import Scanner

console = Console()
app = typer.Typer()


@dataclass
class Compiler:
    scanner: Scanner
    parser: Parser

    def compile(self) -> None:
        try:
            self.parser.parse()
        except Exception as e:
            print(f"{e}")


@app.command()
def main(
    source: Annotated[Path, typer.Argument()],
    debug: bool = False,
) -> None:

    logger.remove()
    if debug:
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    scanner.open(source)
    parser = Parser(scanner=scanner)

    compiler = Compiler(scanner=scanner, parser=parser)
    compiler.compile()


if __name__ == "__main__":
    app()