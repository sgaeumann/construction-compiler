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

from rich.panel import Panel
from rich.pretty import Pretty
import typer
from loguru import logger
from rich.console import Console

from .parser import Parser
from .scanner import Scanner
from .ast import *

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

    def ast(self) -> Syntax:
        return self.parser.parse()


@app.command()
def main(
    source: Annotated[Path, typer.Argument()],
    debug: bool = False,
    show_tree: bool = False,
):

    logger.remove()
    if debug:
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    scanner.open(source)
    parser = Parser(scanner=scanner)

    compiler = Compiler(scanner=scanner, parser=parser)
    ast_ = compiler.ast()

    if ast_ is None:
        console.print("[red]Compilation failed[/red]")
        return
    elif show_tree:
        console.print(Panel(Pretty(ast_, indent_size=2), title="Syntax Tree"))
    else:
        console.print(Panel(ast_.rich(), title="Code"))


if __name__ == "__main__":
    app()
