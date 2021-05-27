from components.preprocessor import PrePro
from components.token import Token
from components.tokenizer import Tokenizer
from components.node import (
    BinOp,
    IntVal,
    BoolVal,
    UnOp,
    Identifier,
    Assign,
    NoOp,
    Block,
    Print,
    Read,
    LogicalOp,
    While,
    If,
    Declare,
    StringVal,
    FunctionDeclare,
    FunctionCall,
    Return,
)


class Parser:
    def __init__(self):
        self.tokens = None

    def parseFactor(self):
        self.tokens.nextToken()
        if self.tokens.actual.type == "INT":
            return IntVal(self.tokens.actual.value)
        elif self.tokens.actual.type == "BOOL":
            return BoolVal(self.tokens.actual.value)
        elif self.tokens.actual.type == "STRING":
            return StringVal(self.tokens.actual.value)
        elif self.tokens.actual.type in ["PLUS", "MINUS", "NOT"]:
            return UnOp(self.tokens.actual.type, [self.parseFactor()])
        elif self.tokens.actual.type == "LPAR":
            exp = self.parseOrExpr()
            if self.tokens.actual.type == "RPAR":
                return exp
            else:
                raise ValueError("Could not close parenthesis")
        elif self.tokens.actual.type == "IDENTIFIER":
            identifier = self.tokens.actual.value
            self.tokens.nextToken()
            if self.tokens.actual.type == "LPAR":
                funcCallArgs = []
                self.tokens.nextToken()
                if self.tokens.actual.type == "RPAR":
                    return FunctionCall(identifier, funcCallArgs)
                else:
                    self.tokens.goBack()
                while self.tokens.actual.type != "RPAR":
                    funcCallArgs += [self.parseOrExpr()]
                    if self.tokens.actual.type == "COMMA":
                        continue
                    if self.tokens.actual.type == "RPAR":
                        break
                    else:
                        raise ValueError("aaaa")
                return FunctionCall(identifier, funcCallArgs)
            else:
                self.tokens.goBack()
                return Identifier(self.tokens.actual.value)
        elif self.tokens.actual.type == "READ":
            self.tokens.nextToken()
            if self.tokens.actual.value != "(":
                raise ValueError("readln must be followed by (")
            self.tokens.nextToken()
            if self.tokens.actual.value != ")":
                raise ValueError("readln( must be followed by )")
            return Read(None)
        else:
            raise ValueError(f"Cannot parse Factor, {self.tokens.actual.type}")

    def parseTerm(self):
        resultado = self.parseFactor()
        self.tokens.nextToken()
        while self.tokens.actual.type in ["MULT", "DIV"]:
            if self.tokens.actual.type in ["MULT", "DIV"]:
                resultado = BinOp(
                    self.tokens.actual.type, [resultado, self.parseFactor()]
                )
            else:
                raise ValueError("Could not complete parseTerm")
            self.tokens.nextToken()
        return resultado

    def parseExpression(self):
        result = self.parseTerm()
        while self.tokens.actual.type in ["PLUS", "MINUS"]:
            if self.tokens.actual.type in ["PLUS", "MINUS"]:
                result = BinOp(self.tokens.actual.type, [result, self.parseTerm()])
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseRelExpr(self):
        result = self.parseExpression()
        while self.tokens.actual.type in ["LESSTHAN", "BIGGERTHAN"]:
            if self.tokens.actual.type in ["LESSTHAN", "BIGGERTHAN"]:
                result = LogicalOp(
                    self.tokens.actual.type, [result, self.parseExpression()]
                )
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseEqExpr(self):
        result = self.parseRelExpr()
        while self.tokens.actual.type in ["EQOP"]:
            if self.tokens.actual.type in ["EQOP"]:
                result = LogicalOp(
                    self.tokens.actual.type, [result, self.parseRelExpr()]
                )
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseAndExpr(self):
        result = self.parseEqExpr()
        while self.tokens.actual.type in ["AND"]:
            if self.tokens.actual.type in ["AND"]:
                result = LogicalOp(
                    self.tokens.actual.type, [result, self.parseEqExpr()]
                )
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseOrExpr(self):
        result = self.parseAndExpr()
        while self.tokens.actual.type in ["OR"]:
            if self.tokens.actual.type in ["OR"]:
                result = LogicalOp(
                    self.tokens.actual.type, [result, self.parseAndExpr()]
                )
            else:
                raise ValueError("Error: it never should reach this")
        return result

    def parseCommand(self):
        if self.tokens.actual.type == "IDENTIFIER":
            identifier = self.tokens.actual.value
            self.tokens.nextToken()
            if self.tokens.actual.type == "EQUAL":
                result = Assign(identifier, [self.parseOrExpr()])
            elif self.tokens.actual.type == "LPAR":
                funcCallArgs = []
                self.tokens.nextToken()
                if self.tokens.actual.type == "RPAR":
                    self.tokens.nextToken()
                    return FunctionCall(identifier, funcCallArgs)
                else:
                    self.tokens.goBack()
                while self.tokens.actual.type != "RPAR":
                    funcCallArgs += [self.parseOrExpr()]
                    if self.tokens.actual.type == "COMMA":
                        continue
                    if self.tokens.actual.type == "RPAR":
                        break
                    else:
                        raise ValueError("aaaa")
                self.tokens.nextToken()
                result = FunctionCall(identifier, funcCallArgs)
            else:
                raise ValueError(
                    f"IDENTIFIERS must be followed by '=' or '(', but got '{self.tokens.actual.value}'"
                )

            if (self.tokens.actual.value) != ";":
                raise ValueError(
                    f"Assign commands must end with ';', but got '{self.tokens.actual.value}'"
                )
            self.tokens.nextToken()

        elif self.tokens.actual.type in ["TYPE_INT", "TYPE_STRING", "TYPE_BOOL"]:
            var_type = self.tokens.actual.type
            self.tokens.nextToken()
            if self.tokens.actual.type != "IDENTIFIER":
                raise ValueError(f"Expected IDENTIFIER after {var_type} declaration.")
            var_name = self.tokens.actual.value
            result = Declare(var_name, [(None, var_type)])
            self.tokens.nextToken()
            if (self.tokens.actual.value) != ";":
                raise ValueError(
                    f"Declare commands must end with ';', but got '{self.tokens.actual.value}'"
                )

            self.tokens.nextToken()

        elif self.tokens.actual.type == "PRINT":
            self.tokens.nextToken()
            if self.tokens.actual.type != "LPAR":
                raise ValueError(
                    f"println must be followed by '(', got '{self.tokens.actual.value}'"
                )
            result = Print(None, [self.parseOrExpr()])
            if self.tokens.actual.type != "RPAR":
                raise ValueError(
                    f"println must end with ')', got '{self.tokens.actual.value}'"
                )
            self.tokens.nextToken()

            if (self.tokens.actual.value) != ";":
                raise ValueError(
                    f"Print commands must end with ';', but got '{self.tokens.actual.value}'"
                )

            self.tokens.nextToken()

        elif self.tokens.actual.type == "WHILE":
            self.tokens.nextToken()
            if self.tokens.actual.type != "LPAR":
                raise ValueError(
                    f"println must be followed by '(', got '{self.tokens.actual.value}'"
                )
            orExpr = self.parseOrExpr()
            if self.tokens.actual.type != "RPAR":
                raise ValueError(
                    f"println must end with ')', got '{self.tokens.actual.value}'"
                )
            self.tokens.nextToken()
            result = While(None, [orExpr, self.parseCommand()])

        elif self.tokens.actual.type == "IF":
            self.tokens.nextToken()
            if self.tokens.actual.type != "LPAR":
                raise ValueError(
                    f"println must be followed by '(', got '{self.tokens.actual.value}'"
                )
            orExpr = self.parseOrExpr()
            if self.tokens.actual.type != "RPAR":
                raise ValueError(
                    f"println must end with ')', got '{self.tokens.actual.value}'"
                )
            self.tokens.nextToken()
            trueBlock = self.parseCommand()
            falseBlock = NoOp(None)
            if self.tokens.actual.type == "ELSE":
                self.tokens.nextToken()
                falseBlock = self.parseCommand()
            result = If(None, [orExpr, trueBlock, falseBlock])

        elif self.tokens.actual.value == "{":
            result = self.parseBlock()
            self.tokens.nextToken()

        elif self.tokens.actual.type == "RETURN":
            result = Return(self.parseOrExpr())

        else:
            result = NoOp(None)
            # cases like +1+2*2; enter here
            # they would raise errors on the next if ";".
            # just to manage errors more precisely, some will be treated here
            if (str(self.tokens.actual.value) in "()+-*/=") or (
                self.tokens.actual.type == "INT"
            ):
                raise ValueError(
                    "Commands must be Assignments or Prints, Ifs or Whiles"
                )

            if (self.tokens.actual.value) != ";":
                raise ValueError(
                    f"Commands must end with ';', but got '{self.tokens.actual.value}'"
                )
            self.tokens.nextToken()

        return result

    def parseBlock(self):
        if self.tokens.actual.value != "{":
            raise ValueError("Block must start with '{'")
        executedCommands = []
        self.tokens.nextToken()
        while self.tokens.actual.value != "}":
            executedCommands += [self.parseCommand()]

        return Block(None, executedCommands)

    def parseFuncDefBlock(self):
        types = [
            "TYPE_INT",
            "TYPE_BOOL",
            "TYPE_STRING",
        ]
        functions = []
        while self.tokens.actual.type in types:
            funcType = self.tokens.actual.type
            self.tokens.nextToken()
            if self.tokens.actual.type != "IDENTIFIER":
                raise ValueError(
                    f"Expected function name, but got '{self.tokens.actual.type}'"
                )
            func_name = self.tokens.actual.value
            self.tokens.nextToken()
            if self.tokens.actual.type != "LPAR":
                raise ValueError(
                    f"FuncDef: Function name must be followed by '(', but got '{self.tokens.actual.type}'"
                )
            self.tokens.nextToken()
            nodeArgs = []
            argNames = []
            while self.tokens.actual.type != "RPAR":
                if self.tokens.actual.type not in types:
                    raise ValueError(f"FuncDef: function arguments must have a type")
                arg_type = self.tokens.actual.type
                self.tokens.nextToken()
                if self.tokens.actual.type != "IDENTIFIER":
                    raise ValueError(
                        f"FuncDef: argument type must be followed by arg name"
                    )
                arg_name = self.tokens.actual.value
                self.tokens.nextToken()
                if self.tokens.actual.type == "COMMA":
                    self.tokens.nextToken()
                nodeArgs += [Declare(arg_name, [(None, arg_type)])]
                argNames += [arg_name]

            if self.tokens.actual.type != "RPAR":
                raise ValueError(
                    f"FuncDef: Function name must be followed by ')', but got '{self.tokens.actual.type}'"
                )
            self.tokens.nextToken()
            funcBlock = self.parseCommand()
            # print(self.tokens.actual.type)

            functions += [
                FunctionDeclare(func_name, [nodeArgs, funcBlock, funcType, argNames])
            ]
        functions += [FunctionCall("main")]
        return Block(None, functions)

    def run(self, code):
        code = PrePro(code).filter()
        PrePro(code).check_PAR_balance()
        self.tokens = Tokenizer(code)
        self.tokens.tokenize()

        self.tokens.nextToken()
        result = self.parseFuncDefBlock()

        if self.tokens.actual.type != "EOF":
            raise ValueError("Did not reach EOF")
        return result