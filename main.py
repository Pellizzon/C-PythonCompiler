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
        allowed_symbols = ["+", "-", "*", "/", " "]

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
            else:
                raise ValueError("Erro")

        # whenever the loop ends, we must add the last number to the tokens:
        if number != "":
            self.tokens.append(Token("INT", int(number)))
        # it's also needed to add the EOF Token:
        self.tokens.append(Token("EOF", None))

    def returnNextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1
        return self.actual


class PrePro:
    def __init__(self, initCode):
        self.code = initCode

    def filter(self):
        return re.sub(r"/\*.*?\*/", "", self.code)


class Parser:
    def __init__(self):
        self.tokens = None

    def parseTerm(self):
        symbols = ["MULT", "DIV"]

        t = self.tokens.returnNextToken()
        if t.type == "INT":
            resultado = t.value
            t = self.tokens.returnNextToken()
            while t.type in symbols:
                if t.type == "MULT":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado *= t.value
                    else:
                        continue
                elif t.type == "DIV":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado /= t.value
                    else:
                        continue
                t = self.tokens.returnNextToken()
            nextToken = t
            return int(resultado), nextToken
        else:
            raise ValueError("Erro")

    def parseExpression(self):
        symbols = ["PLUS", "MINUS"]

        resultTerm, token = self.parseTerm()
        resultado = resultTerm
        while token.type in symbols:
            if token.type == "PLUS":
                resultTerm, token = self.parseTerm()
                resultado += resultTerm
            elif token.type == "MINUS":
                resultTerm, token = self.parseTerm()
                resultado -= resultTerm
            else:
                raise ValueError("Erro")
        if token.type == "EOF":
            return int(resultado)
        else:
            raise ValueError("Erro")

    def run(self, code):
        code = PrePro(code).filter()
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()
        print(self.parseExpression())


if __name__ == "__main__":

    Parser().run(sys.argv[1])
