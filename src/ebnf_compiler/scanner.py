# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Scanner
"""

import typing
from dataclasses import dataclass
from pathlib import Path

import typer
from loguru import logger
from rich import print
from rich.console import Console

from .tokens import Token

console = Console()


@dataclass
class Scanner:
    eof: bool = False
    sym: Token | None = None  # Next Symbol
    value: str = ""

    _ch: str = ""
    _file_name: Path | None = None
    _text: typing.TextIO | None = None
    _text_line: str = ""
    _line_no: int = 0
    _col_no: int = 0

    # static
    token_map: typing.ClassVar[dict[str, Token]] = {
        "=": Token.EQL,
        "(": Token.LPAREN,
        ")": Token.RPAREN,
        "[": Token.LBRAK,
        "]": Token.RBRAK,
        "{": Token.LBRACE,
        "}": Token.RBRACE,
        "|": Token.BAR,
        ".": Token.PERIOD,
    }

    # TextIO : file, string converted to file
    def init(self, f: typing.TextIO) -> None:
        self._text = f
        self.get_next_char()

    def open(self, file_name: Path) -> None:
        logger.debug(f"Opening {file_name}")
        self._file_name = file_name
        try:
            f = self._file_name.open("r")
            self.init(f)
        except Exception:
            print(f"[bold red]Error: Source file '{file_name}' not found[/bold red]")
            raise typer.Exit(code=1) from None

    def print_error(self, msg: str):
        console.print(
            f"Error: {msg}"
            f"(File {self._file_name}, Line {self._line_no}, Column {self._col_no})"
        )

    def skip_space(self) -> None:
        while self._ch.isspace():
            self.get_next_char()

    def get_next_char(self) -> None:
        if self._text is None:
            raise Exception("Scanner not initialized")
        while not self.eof and self._text_line == "":
            self._text_line = self._text.readline()
            self._line_no += 1
            self._col_no = 0
            if self._text_line == "":
                self.eof = True
                break
            self._text_line = self._text_line.rstrip()
        if self.eof:
            self._ch = ""
        else:
            assert self._text_line != ""
            self._ch = self._text_line[0]
            self._text_line = self._text_line[1:]
            self._col_no += 1

    def get_next_symbol(self):
        self.skip_space()
        if self._ch.isalpha():
            self.sym = Token.IDENT
            self.value = self._ch
            self.get_next_char()
            while self._ch.isalpha():
                self.value += self._ch
                self.get_next_char()

        elif self._ch == '"':
            self.sym = Token.LITERAL
            self.value = ""
            self.get_next_char()
            while not self.eof and self._ch != '"':
                self.value += self._ch
                self.get_next_char()
            if self.eof:
                self.print_error("Unterminated literal")
                return
            self.get_next_char()
        elif self._ch == "":
            self.sym = Token.EOF
            self.value = ""
        elif self._ch in self.token_map:
            self.sym = self.token_map[self._ch]
            self.value = self._ch
            self.get_next_char()
        else:
            self.sym = Token.OTHER
            self.value = self._ch
            self.get_next_char()
        logger.info(f"Token: {self.sym}, Value: {self.value}")