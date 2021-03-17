import sys
import re


class Token:
    def __init__(self, initType, initValue):
        self.type = initType
        self.value = initValue


class Tokenizer:
    def __init__(self, initOrigin):
        self.origin = initOrigin
        self.position = 0
        self.tokens = []
        self.actual = None

    def tokenize(self):
        # " " is allowed, however the compiler ignores it
        allowed_symbols = ["+", "-", "*", "/", " ", "(", ")"]

        number = ""
        for i in self.origin:
            if i.isdigit():
                number += i
                continue
            elif i in allowed_symbols:
                # whenever we find an operator, we add the number;
                # it was already found
                if number != "":
                    self.tokens.append(Token("INT", int(number)))
                    number = ""
                if i == "+":
                    self.tokens.append(Token("PLUS", "+"))
                elif i == "-":
                    self.tokens.append(Token("MINUS", "-"))
                elif i == "*":
                    self.tokens.append(Token("MULT", "*"))
                elif i == "/":
                    self.tokens.append(Token("DIV", "/"))
                elif i == "(":
                    self.tokens.append(Token("LPAR", "("))
                elif i == ")":
                    self.tokens.append(Token("RPAR", ")"))
            else:
                raise ValueError("Found invalid character in code")

        # whenever the loop ends, we must add the last number to the tokens:
        if number != "":
            self.tokens.append(Token("INT", int(number)))
        # it's also needed to add the EOF Token:
        self.tokens.append(Token("EOF", None))

        # for i in self.tokens:
        #     print(i.type, i.value)

    def nextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1


class PrePro:
    def __init__(self, initCode):
        self.code = initCode

    def filter(self):
        return re.sub(r"/\*.*?\*/", "", self.code)

    def check_PAR_balance(self):
        stack = []
        for i in self.code:
            if i == "(":
                stack.append(i)
            elif i == ")":
                if len(stack) > 0:
                    stack.pop()
                else:
                    raise ValueError("Found closing parenthesis, but stack was empty")
        if len(stack) != 0:
            raise ValueError("Code is unbalanced")


class Parser:
    def __init__(self):
        self.tokens = None

    def parseFactor(self):
        self.tokens.nextToken()
        if self.tokens.actual.type == "INT":
            return self.tokens.actual.value
        elif self.tokens.actual.type == "PLUS":
            return self.parseFactor()
        elif self.tokens.actual.type == "MINUS":
            return -self.parseFactor()
        elif self.tokens.actual.type == "LPAR":
            exp = self.parseExpression()
            if self.tokens.actual.type == "RPAR":
                return exp
            else:
                raise ValueError("Could not close parenthesis")

    def parseTerm(self):
        symbols = ["MULT", "DIV"]

        factor = self.parseFactor()
        resultado = factor
        self.tokens.nextToken()
        while self.tokens.actual.type in symbols:
            if self.tokens.actual.type == "MULT":
                factor = self.parseFactor()
                resultado *= factor
            elif self.tokens.actual.type == "DIV":
                factor = self.parseFactor()
                resultado /= factor
            self.tokens.nextToken()
        return int(resultado)

    def parseExpression(self):
        symbols = ["PLUS", "MINUS"]

        resultTerm = self.parseTerm()
        resultado = resultTerm
        while self.tokens.actual.type in symbols:
            if self.tokens.actual.type == "PLUS":
                resultTerm = self.parseTerm()
                resultado += resultTerm
            elif self.tokens.actual.type == "MINUS":
                resultTerm = self.parseTerm()
                resultado -= resultTerm
            else:
                raise ValueError("Error: it never should reach this")

        return int(resultado)

    def parse(self):
        resultado = self.parseExpression()
        return int(resultado)
        if self.tokens.actual.type == "EOF":
            return int(resultado)
        else:
            raise ValueError("Did not reach EOF")

    def run(self, code):
        code = PrePro(code).filter()
        PrePro(code).check_PAR_balance()
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()
        print(self.parse())


if __name__ == "__main__":

    Parser().run(sys.argv[1])
