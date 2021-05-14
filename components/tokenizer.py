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
            "\t",
            "(",
            ")",
            "=",
            ";",
            "{",
            "}",
            "<",
            ">",
            "!",
            '"',
        ]

        self.double_allowed_symbols = [
            "||",
            "&&",
            "==",
        ]

    def findCompleteIdentifier(self, currentPos):
        rest = ""
        for i in self.origin[currentPos:]:
            if i in ["|", "&"]:
                break
            elif i not in self.allowed_symbols:
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
                if identifier == "int":
                    self.tokens.append(Token("TYPE_INT", identifier))
                elif identifier == "bool":
                    self.tokens.append(Token("TYPE_BOOL", identifier))
                elif identifier == "string":
                    self.tokens.append(Token("TYPE_STRING", identifier))
                elif identifier in ["true", "false"]:
                    self.tokens.append(Token("BOOL", identifier))
                elif identifier == "println":
                    self.tokens.append(Token("PRINT", identifier))
                elif identifier == "readln":
                    self.tokens.append(Token("READ", identifier))
                elif identifier == "if":
                    self.tokens.append(Token("IF", identifier))
                elif identifier == "else":
                    self.tokens.append(Token("ELSE", identifier))
                elif identifier == "while":
                    self.tokens.append(Token("WHILE", identifier))
                else:
                    self.tokens.append(Token("IDENTIFIER", identifier))
                i += len(identifier)

            elif self.origin[i].isdigit():
                number += self.origin[i]
                i += 1

            elif self.origin[i : i + 2] in self.double_allowed_symbols:
                if number != "":
                    self.tokens.append(Token("INT", int(number)))
                    number = ""

                if self.origin[i : i + 2] == "&&":
                    self.tokens.append(Token("AND", "&&"))
                elif self.origin[i : i + 2] == "==":
                    self.tokens.append(Token("EQOP", "=="))
                elif self.origin[i : i + 2] == "||":
                    self.tokens.append(Token("OR", "||"))
                else:
                    raise ValueError(f"Found invalid token in code '{self.origin[i]}'")
                i += 2

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
                    self.tokens.append(Token("LBRACKET", "{"))
                elif self.origin[i] == "}":
                    self.tokens.append(Token("RBRACKET", "}"))
                elif self.origin[i] == ";":
                    self.tokens.append(Token("SEMICOL", ";"))
                elif self.origin[i] == "<":
                    self.tokens.append(Token("LESSTHAN", "<"))
                elif self.origin[i] == ">":
                    self.tokens.append(Token("BIGGERTHAN", ">"))
                elif self.origin[i] == "!":
                    self.tokens.append(Token("NOT", "!"))
                elif self.origin[i] == "=":
                    self.tokens.append(Token("EQUAL", "="))
                elif self.origin[i] == '"':
                    i += 1
                    whole_string = '"'
                    while self.origin[i] != '"':
                        whole_string += self.origin[i]
                        i += 1
                    whole_string += '"'
                    self.tokens.append(Token("STRING", whole_string))
                i += 1

            else:
                if self.origin[i] == "_":
                    raise ValueError(f"Variables cannot start with '{self.origin[i]}'")
                raise ValueError(f"Found invalid character in code '{self.origin[i]}'")

        # for i in self.tokens:
        #     print(i.type, i.value)

        # it's needed to add the EOF Token:
        self.tokens.append(Token("EOF", None))

    def nextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1