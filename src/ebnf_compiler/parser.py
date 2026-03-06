# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Parser
"""

from dataclasses import dataclass

from loguru import logger

from .scanner import Scanner
from .tokens import Token
from .ast import *


@dataclass
class Parser:
    scanner: Scanner
    #ast_root: Node # root node of AST
    has_error: bool = False

    def raise_error(self, msg: str) -> None:
        self.has_error = True
        self.scanner.print_error(msg)
        raise Exception(msg)

    def raise_expected_error(self, expected: Token):
        self.raise_error(f"Expected '{expected}', but got '{self.scanner.sym}'")

    def factor(self) -> Factor:
        logger.debug("Factor")
        sym = self.scanner.sym
        if sym == Token.IDENT:
            # production.identifier.value = ...
            ident = Identifier(self.scanner.value)
            self.scanner.get_next_symbol()
            return ident
        elif sym == Token.LITERAL:
            # production.literal.value = ...
            lit = Literal(value= self.scanner.value)
            self.scanner.get_next_symbol()
            return lit
        elif sym == Token.LPAREN:
            self.scanner.get_next_symbol()
            expr: Expression = self.expression()
            expr.paren = True
            if self.scanner.sym != Token.RPAREN:
                self.raise_expected_error(Token.RPAREN)
            self.scanner.get_next_symbol()
            return expr
        elif sym == Token.LBRAK:
            self.scanner.get_next_symbol()
            opt = Option(expr= self.expression())
            self.expression()
            if self.scanner.sym != Token.RBRAK:
                self.raise_expected_error(Token.RBRAK)
            self.scanner.get_next_symbol()
            return opt
        elif sym == Token.LBRACE:
            self.scanner.get_next_symbol()
            rep = Repetition(expr= self.expression())
            if self.scanner.sym != Token.RBRACE:
                self.raise_expected_error(Token.RBRACE)
            self.scanner.get_next_symbol()
            return rep
        else:
            self.raise_error(
                f"Expected identifier, literal, (', '['. or '{{' got {sym}"
            )
            raise Exception("Unexpected symbol")

    def term(self) -> Term:
        logger.debug("Term")
        # append factor in term.factor
        t = Term([self.factor()])
        while self.scanner.sym in (
            Token.IDENT,
            Token.LITERAL,
            Token.LPAREN,
            Token.LBRAK,
            Token.LBRACE,
        ):
            # append factor in term.factor
            t.factors.append(self.factor())
        return t

    def expression(self) -> Expression:
        logger.debug("Expression")
        # append factor in production.expression.terms
        expr = Expression(terms = [self.term()])
        while self.scanner.sym == Token.BAR:
            self.scanner.get_next_symbol()
            # append factor in production.expression.terms
            expr.terms.append(self.term())
        return expr

    def production(self) -> Production:
        logger.debug("Production")
        if self.scanner.sym != Token.IDENT:
            self.raise_expected_error(Token.IDENT)
        # production.identifier = ...
        ident = Identifier(self.scanner.value)
        self.scanner.get_next_symbol()
        if self.scanner.sym != Token.EQL:
            self.raise_expected_error(Token.EQL)
        self.scanner.get_next_symbol()
        # production.expression = ...
        prod = Production(identifier=ident, expression=self.expression())
        if self.scanner.sym != Token.PERIOD:
            self.raise_expected_error(Token.PERIOD)
        self.scanner.get_next_symbol()
        return prod

    def syntax(self) -> Syntax:
        logger.debug("Syntax")
        # create syntax node
        #self.ast_root = Syntax([])
        ast = Syntax([])
        while self.scanner.sym != Token.EOF:
            if self.scanner.sym != Token.IDENT:
                self.raise_expected_error(Token.IDENT)
            ast.production.append(self.production())
        return ast

    def parse(self) -> Syntax:
        logger.debug("Parsing")
        self.scanner.get_next_symbol()
        return self.syntax()
