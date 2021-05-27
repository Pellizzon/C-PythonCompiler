from components.tables import FunctionTable, SymbolTable

ft = FunctionTable()


class Node:
    def __init__(self, initValue, initChildren=[]):
        self.value = initValue
        self.children = initChildren

    def Evaluate(self, symbolTable):
        return


# Deals with binary operations,
# must have two children
class BinOp(Node):
    def Evaluate(self, symbolTable):
        firstChildValue, firstChildType = self.children[0].Evaluate(symbolTable)
        secondChildValue, secondChildType = self.children[1].Evaluate(symbolTable)

        if firstChildType == "TYPE_STRING":
            raise ValueError(
                f"Cannot handle operation between {firstChildType} and {secondChildType}"
            )
        elif secondChildType == "TYPE_STRING":
            raise ValueError(
                f"Cannot handle operation between {firstChildType} and {secondChildType}"
            )

        if self.value == "PLUS":
            evaluate = firstChildValue + secondChildValue
        elif self.value == "MINUS":
            evaluate = firstChildValue - secondChildValue
        elif self.value == "DIV":
            evaluate = firstChildValue / secondChildValue
        elif self.value == "MULT":
            evaluate = firstChildValue * secondChildValue
        else:
            raise ValueError("Could not evaluate BinOp")

        return (int(evaluate), "TYPE_INT")


# Deals with Logical operations,
# must have two children
class LogicalOp(Node):
    def Evaluate(self, symbolTable):
        firstChildValue, firstChildType = self.children[0].Evaluate(symbolTable)
        secondChildValue, secondChildType = self.children[1].Evaluate(symbolTable)

        if firstChildType == "TYPE_STRING" and secondChildType != "TYPE_STRING":
            raise ValueError(
                f"Cannot handle operation between {firstChildType} and {secondChildType}"
            )
        elif firstChildType != "TYPE_STRING" and secondChildType == "TYPE_STRING":
            raise ValueError(
                f"Cannot handle operation between {firstChildType} and {secondChildType}"
            )
        elif firstChildType == "TYPE_STRING" and secondChildType == "TYPE_STRING":
            if self.value == "EQOP":
                evaluate = firstChildValue == secondChildValue
                return (int(bool(evaluate)), "TYPE_BOOL")
            else:
                raise ValueError(f"Operation {self.value} not allowed between strings")

        if self.value == "LESSTHAN":
            evaluate = firstChildValue < secondChildValue
        elif self.value == "BIGGERTHAN":
            evaluate = firstChildValue > secondChildValue
        elif self.value == "EQOP":
            evaluate = firstChildValue == secondChildValue
        elif self.value == "AND":
            evaluate = firstChildValue and secondChildValue
        elif self.value == "OR":
            evaluate = firstChildValue or secondChildValue
        else:
            raise ValueError("Could not evaluate LogicalOp")

        return (int(bool(evaluate)), "TYPE_BOOL")


# Deals with unary operations,
# must have one child
class UnOp(Node):
    def Evaluate(self, symbolTable):
        childValue, childType = self.children[0].Evaluate(symbolTable)

        if childType == "TYPE_STRING":
            raise ValueError("Cannot handle unary operation with strings")

        if self.value == "PLUS":
            evaluate = +childValue
        elif self.value == "MINUS":
            evaluate = -childValue
        elif self.value == "NOT":
            evaluate = not childValue
            return (int(evaluate), "TYPE_BOOL")
        else:
            raise ValueError("Could not evaluate UnOp")

        return (int(evaluate), "TYPE_INT")


# Returns its own value, it's a "number" node
class IntVal(Node):
    def Evaluate(self, symbolTable):
        return (int(self.value), "TYPE_INT")


# Returns its own bool value, it's a "boolean" node
class BoolVal(Node):
    def Evaluate(self, symbolTable):
        return (int(self.value == "true"), "TYPE_BOOL")


# Returns its own string value, it's a "string" node
class StringVal(Node):
    def Evaluate(self, symbolTable):
        return (str(self.value), "TYPE_STRING")


# no operation
class NoOp(Node):
    def Evaluate(self, symbolTable):
        return super().Evaluate(symbolTable)


# Assigns an identifier (received by self.value/initValue)
# to it's actual value (self.children[0].Evaluate(symbolTable));
# Sets an Identfier's value on the Symbol Table
class Assign(Node):
    def Evaluate(self, symbolTable):
        if symbolTable.contains(self.value):
            var_type = symbolTable.getType(self.value)
            # print(self.children[0].Evaluate(symbolTable))
            childValue, _ = self.children[0].Evaluate(symbolTable)
            if var_type == "TYPE_BOOL":
                symbolTable.set_(self.value, (int(bool(childValue)), var_type))
            elif var_type == "TYPE_INT":
                symbolTable.set_(self.value, (int(childValue), var_type))
            elif var_type == "TYPE_STRING":
                symbolTable.set_(self.value, (str(childValue), var_type))
            else:
                raise ValueError("Unkown type.")
        else:
            raise ValueError(f"Set on undeclared variable '{self.value}'")


# Contary to the Assign object, Identifier used to get
# an identifier's value from the Symbol Table
class Identifier(Node):
    def Evaluate(self, symbolTable):
        # ST is responsible for returning variable value and type
        return symbolTable.get(self.value)


class Declare(Node):
    def Evaluate(self, symbolTable):
        symbolTable.declare(self.value, self.children[0])


class While(Node):
    def Evaluate(self, symbolTable):
        _, childrenType = self.children[0].Evaluate(symbolTable)
        if childrenType == "TYPE_STRING":
            raise ValueError("while(TYPE_STRING) is not allowed")
        # conditional child
        while self.children[0].Evaluate(symbolTable)[0]:
            # block or command child
            self.children[1].Evaluate(symbolTable)


class If(Node):
    def Evaluate(self, symbolTable):
        childrenValue, childrenType = self.children[0].Evaluate(symbolTable)
        if childrenType == "TYPE_STRING":
            raise ValueError("if(TYPE_STRING) is not allowed")

        if childrenValue:
            # block or command child 1
            self.children[1].Evaluate(symbolTable)
        else:
            # block or command child 2
            self.children[2].Evaluate(symbolTable)


# prints a value
# composed by identifiers and/or expressions
class Print(Node):
    def Evaluate(self, symbolTable):
        childValue, childType = self.children[0].Evaluate(symbolTable)

        if childType == "TYPE_INT":
            print(childValue)
        elif childType == "TYPE_BOOL":
            print("true") if childValue == 1 else print("false")
        elif childType == "TYPE_STRING":
            print(childValue.replace('"', ""))


# receives an user input
# Value and Children are not needed
class Read(Node):
    def Evaluate(self, symbolTable):
        return (int(input()), "TYPE_INT")


# A Block can have many instructions. Each line of code
# (instruction) is added as a child of block.
# When each child is evaluated, Assigns and Identifiers are
# being used to build the symbol table and eventualy
# Print a result
class Block(Node):
    def Evaluate(self, symbolTable):
        for i in self.children:
            i.Evaluate(symbolTable)
            # necessary for recursion purposes and to quit a function
            # as soon as return is called
            if symbolTable.contains("return"):
                return symbolTable.get("return")


class FunctionDeclare(Node):
    def Evaluate(self, symbolTable):
        funcArgsNames = self.children[0]
        funcBlock = self.children[1]
        funcType = self.children[2]
        ft.newFunc(self.value, funcBlock, funcType, funcArgsNames)


class FunctionCall(Node):
    def Evaluate(self, symbolTable):
        funcSt = SymbolTable()
        funcArgs = ft.getFuncArgs(self.value)
        if len(funcArgs) != len(self.children):
            raise ValueError("Number of arguments mismatch")
        for i in range(len(funcArgs)):
            childEval = self.children[i].Evaluate(symbolTable)
            argumentIdentifier, argumentType = funcArgs[i]
            if argumentType == "TYPE_STRING" and childEval[1] in [
                "TYPE_BOOL, TYPE_INT"
            ]:
                raise ValueError(
                    f"argument '{argumentIdentifier}' of function '{self.value}' declared as '{argumentType}', but got '{childEval[1]}'"
                )
            elif (
                argumentType in ["TYPE_BOOL, TYPE_INT"]
                and childEval[1] == "TYPE_STRING"
            ):
                raise ValueError(
                    f"argument '{argumentIdentifier}' of function '{self.value}' declared as '{argumentType}', but got '{childEval[1]}'"
                )
            funcSt.set_(argumentIdentifier, childEval)

        ft.getFuncBlock(self.value).Evaluate(funcSt)

        if funcSt.contains("return"):
            return_val = funcSt.get("return")[0]
            function_type = ft.getFuncType(self.value)
            if function_type == "TYPE_BOOL":
                funcSt.set_("return", (int(bool(return_val)), function_type))
            elif function_type == "TYPE_INT":
                funcSt.set_("return", (int(return_val), function_type))
            elif function_type == "TYPE_STRING":
                funcSt.set_("return", (str(return_val), function_type))
            else:
                raise ValueError("Unkown type.")
            return funcSt.get("return")


class Return(Node):
    def Evaluate(self, symbolTable):
        symbolTable.set_("return", self.value.Evaluate(symbolTable))
