from components.token import Token


class Tokenizer:
    def __init__(self, initOrigin):
        self.origin = initOrigin
        self.position = 0
        self.tokens = []
        self.actual = None
        # " " && "\n" are allowed, however they are ignored
        self.allowed_symbols = [
            "+",
            "-",
            "*",
            "/",
            " ",
            "\n",
            "(",
            ")",
            "{",
            "}",
            "=",
            ";",
        ]

    def findCompleteIdentifier(self, currentPos):
        rest = ""
        for i in self.origin[currentPos:]:
            if i not in self.allowed_symbols:
                rest += i
            else:
                break
        return rest

    def tokenize(self):
        number = ""
        i = 0
        while i < len(self.origin):
            if self.origin[i].isalpha():
                identifier = self.findCompleteIdentifier(i)
                if identifier == "println":
                    self.tokens.append(Token("PRINT", identifier))
                else:
                    self.tokens.append(Token("IDENTIFIER", identifier))
                i += len(identifier)

            elif self.origin[i].isdigit():
                number += self.origin[i]
                i += 1

            elif self.origin[i] in self.allowed_symbols:
                if number != "":
                    self.tokens.append(Token("INT", int(number)))
                    number = ""
                if self.origin[i] == "+":
                    self.tokens.append(Token("PLUS", "+"))
                elif self.origin[i] == "-":
                    self.tokens.append(Token("MINUS", "-"))
                elif self.origin[i] == "*":
                    self.tokens.append(Token("MULT", "*"))
                elif self.origin[i] == "/":
                    self.tokens.append(Token("DIV", "/"))
                elif self.origin[i] == "(":
                    self.tokens.append(Token("LPAR", "("))
                elif self.origin[i] == ")":
                    self.tokens.append(Token("RPAR", ")"))
                elif self.origin[i] == "{":
                    self.tokens.append(Token("LBRA", "{"))
                elif self.origin[i] == "}":
                    self.tokens.append(Token("RBRA", "}"))
                elif self.origin[i] == "=":
                    self.tokens.append(Token("EQ", "="))
                elif self.origin[i] == ";":
                    self.tokens.append(Token("COL", ";"))
                i += 1
            else:
                raise ValueError("Found invalid character in code")

        # it's needed to add the EOF Token:
        self.tokens.append(Token("EOF", None))

    def nextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1