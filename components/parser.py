from components.preprocessor import PrePro
from components.token import Token
from components.tokenizer import Tokenizer
from components.node import BinOp, IntVal, UnOp


class Parser:
    def __init__(self):
        self.tokens = None

    def parseFactor(self):
        self.tokens.nextToken()
        if self.tokens.actual.type == "INT":
            return IntVal(self.tokens.actual.value)
        elif self.tokens.actual.type == "PLUS":
            return UnOp("PLUS", [self.parseFactor()])
        elif self.tokens.actual.type == "MINUS":
            return UnOp("MINUS", [self.parseFactor()])
        elif self.tokens.actual.type == "LPAR":
            exp = self.parseExpression()
            if self.tokens.actual.type == "RPAR":
                return exp
            else:
                raise ValueError("Could not close parenthesis")
        else:
            raise ValueError("Cannot parse Factor")

    def parseTerm(self):
        symbols = ["MULT", "DIV"]

        resultado = self.parseFactor()
        self.tokens.nextToken()
        while self.tokens.actual.type in symbols:
            if self.tokens.actual.type == "MULT":
                factor = self.parseFactor()
                resultado = BinOp("MULT", [resultado, factor])
            elif self.tokens.actual.type == "DIV":
                factor = self.parseFactor()
                resultado = BinOp("DIV", [resultado, factor])
            else:
                raise ValueError("Could not complete parseTerm")
            self.tokens.nextToken()
        return resultado

    def parseExpression(self):
        symbols = ["PLUS", "MINUS"]

        resultTerm = self.parseTerm()
        resultado = resultTerm
        while self.tokens.actual.type in symbols:
            if self.tokens.actual.type == "PLUS":
                resultTerm = self.parseTerm()
                resultado = BinOp("PLUS", [resultado, resultTerm])
            elif self.tokens.actual.type == "MINUS":
                resultTerm = self.parseTerm()
                resultado = BinOp("MINUS", [resultado, resultTerm])
            else:
                raise ValueError("Error: it never should reach this")

        return resultado

    def parse(self):
        resultado = self.parseExpression()
        if self.tokens.actual.type == "EOF":
            return resultado
        else:
            raise ValueError("Did not reach EOF")

    def run(self, code):
        code = PrePro(code).filter()
        PrePro(code).check_PAR_balance()
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()
        return self.parse()