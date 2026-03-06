# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Abstract Syntax Tree
"""

from dataclasses import dataclass
import rich


@dataclass
class Node:
    terminal_sym = {}
    sym = {}   



@dataclass
class Factor(Node):
    def rich(self) -> str:
        return (
            f""
        )


@dataclass
class Term(Node):
    factors: list[Factor]

    def rich(self) -> str:
        return (
            f"[magenta]{[factor.rich() for factor in self.factors]}[/magenta]"
        )


@dataclass
class Identifier(Factor):
    value: str

    def rich(self) -> str:
        return (
            f"{self.value}"
        )


@dataclass
class Literal(Factor):
    value: str

    def rich(self) -> str:
        return (
            f"{self.value}"
        )


@dataclass
class Expression(Factor):
    terms: list[Term]
    paren: bool = False

    def rich(self) -> str:
        if self.paren:
            return (
                f"[cyan]([/cyan] {[term.rich() for term in self.terms]}[cyan])[/cyan]"
            )
        return (
            f"{[term.rich() for term in self.terms]}"
        )  


@dataclass
class Option(Factor):
    expr: Expression

    def rich(self) -> str:
        return (
            f"[cyan][[/cyan]{self.expr.rich()}[cyan]][/cyan]"
        )


@dataclass
class Repetition(Factor):
    expr: Expression

    def rich(self) -> str:
        return (
            f"[cyan]{{[/cyan] {self.expr.rich()} [cyan]}}[/cyan]"
        )


@dataclass
class Production(Node):
    identifier: Identifier
    expression: Expression

    def rich(self) -> str:
        return (
            f"[yellow]{self.identifier.rich()}[/yellow] [cyan]=[/cyan] "
            f"{self.expression.rich()}[cyan].[/cyan]"
        )


@dataclass
class Syntax(Node):
    production: list[Production]

    def rich(self) -> str:
        return (
            f":raccoon:\t AST \t :raccoon:\n{"\n".join([prod.rich() for prod in self.production])}"
        )