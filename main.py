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
        allowed_symbols = ["+", "-", "*", "-", " "]

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
        self.tokens.append(Token("INT", int(number)))
        # it's also needed to add the EOF Token:
        self.tokens.append(Token("EOF", None))

        # # https://stackoverflow.com/questions/691148/pythonic-way-to-implement-a-tokenizer
        # scanner = re.Scanner(
        #     [
        #         (r"[0-9]+", lambda scanner, token: Token("INT", int(token))),
        #         (r"\+", lambda scanner, token: Token("PLUS", token)),
        #         (r"-", lambda scanner, token: Token("MINUS", token)),
        #         (r"\*", lambda scanner, token: Token("MULT", token)),
        #         (r"/", lambda scanner, token: Token("DIV", token)),
        #         (r"\w+", lambda scanner, token: Token("TRASH", None)),
        #         (r"\s+", None),
        #     ]
        # )

        # results, remainder = scanner.scan(self.origin)

        # results.append(Token("EOF", None))

        # self.tokens = results

        # for i in list(self.tokens):
        #     print(i.type, i.value)

    def returnNextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1
        return self.actual


class Parser:
    def __init__(self):
        self.tokens = None

    def parseExpression(self):
        symbols = ["PLUS", "MINUS", "MULT", "DIV"]

        t = self.tokens.returnNextToken()
        if t.type == "INT":
            resultado = t.value
            t = self.tokens.returnNextToken()
            while t.type in symbols:
                if t.type == "PLUS":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado += t.value
                    else:
                        raise ValueError("Erro")
                elif t.type == "MINUS":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado -= t.value
                    else:
                        raise ValueError("Erro")
                elif t.type == "MULT":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado *= t.value
                    else:
                        raise ValueError("Erro")
                elif t.type == "DIV":
                    t = self.tokens.returnNextToken()
                    if t.type == "INT":
                        resultado /= t.value
                    else:
                        raise ValueError("Erro")
                else:
                    raise ValueError("Erro")
                t = self.tokens.returnNextToken()
            if t.type == "EOF":
                return resultado
            else:
                raise ValueError("Erro")
        else:
            raise ValueError("Erro")

    def run(self, code):
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()
        print(self.parseExpression())


if __name__ == "__main__":

    Parser().run(sys.argv[1])
