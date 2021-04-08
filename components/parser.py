from components.preprocessor import PrePro
from components.token import Token
from components.tokenizer import Tokenizer
from components.node import (
    BinOp,
    IntVal,
    UnOp,
    Identifier,
    Assign,
    NoOp,
    Block,
    Print,
)
from components.symbolTable import SymbolTable


class Parser:
    def __init__(self):
        self.tokens = None

    def parseFactor(self):
        self.tokens.nextToken()
        tokenType = self.tokens.actual.type
        if tokenType == "INT":
            return IntVal(self.tokens.actual.value)
        elif tokenType in ["PLUS", "MINUS"]:
            return UnOp(tokenType, [self.parseFactor()])
        elif tokenType == "LPAR":
            exp = self.parseExpression()
            if self.tokens.actual.type == "RPAR":
                return exp
            else:
                raise ValueError("Could not close parenthesis")
        elif tokenType == "IDENTIFIER":
            return Identifier(self.tokens.actual.value)
        else:
            raise ValueError("Cannot parse Factor")

    def parseTerm(self):
        resultado = self.parseFactor()
        self.tokens.nextToken()
        while self.tokens.actual.type in ["MULT", "DIV"]:
            if self.tokens.actual.type in ["MULT", "DIV"]:
                currentToken = self.tokens.actual.type
                factor = self.parseFactor()
                resultado = BinOp(currentToken, [resultado, factor])
            else:
                raise ValueError("Could not complete parseTerm")
            self.tokens.nextToken()
        return resultado

    def parseExpression(self):
        result = self.parseTerm()
        while self.tokens.actual.type in ["PLUS", "MINUS"]:
            if self.tokens.actual.type in ["PLUS", "MINUS"]:
                currentToken = self.tokens.actual.type
                resultTerm = self.parseTerm()
                result = BinOp(currentToken, [result, resultTerm])
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseCommand(self):
        if self.tokens.actual.type == "IDENTIFIER":
            identifier = self.tokens.actual.value
            self.tokens.nextToken()
            if self.tokens.actual.type != "EQ":
                raise ValueError(
                    f"Assigning a variable must receive an '=', but got {self.tokens.actual.value}"
                )
            result = Assign(identifier, [self.parseExpression()])

        elif self.tokens.actual.type == "PRINT":
            self.tokens.nextToken()
            if self.tokens.actual.type != "LPAR":
                raise ValueError(
                    f"println must be followed by '(', got {self.tokens.actual.value}"
                )
            result = Print(None, [self.parseExpression()])
            if self.tokens.actual.type != "RPAR":
                raise ValueError(
                    f"println must end with ')', got {self.tokens.actual.value}"
                )
            self.tokens.nextToken()

        else:
            result = NoOp(None)

        if (self.tokens.actual.value) != ";":
            raise ValueError("Assignments must end with ';'")

        self.tokens.nextToken()
        return result

    def parseBlock(self):
        executedCommands = []
        self.tokens.nextToken()
        while self.tokens.actual.type != "EOF":
            executedCommands += [self.parseCommand()]

        return Block(None, executedCommands)

    def run(self, code):
        code = PrePro(code).filter()
        PrePro(code).check_PAR_balance()
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()
        return self.parseBlock()