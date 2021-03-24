from components.token import Token


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