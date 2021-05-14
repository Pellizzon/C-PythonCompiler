from components.symbolTable import SymbolTable

symbolTable = SymbolTable()


class Node:
    def __init__(self, initValue, initChildren=[]):
        self.value = initValue
        self.children = initChildren

    def Evaluate(self):
        return


# Deals with binary operations,
# must have two children
class BinOp(Node):
    def Evaluate(self):
        firstChildValue, firstChildType = self.children[0].Evaluate()
        secondChildValue, secondChildType = self.children[1].Evaluate()

        if firstChildType == "TYPE_STRING" and secondChildType != "TYPE_STRING":
            raise ValueError(
                f"Cannot handle operation between {firstChildType} and {secondChildType}"
            )
        elif firstChildType != "TYPE_STRING" and secondChildType == "TYPE_STRING":
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

        if firstChildType == "TYPE_STRING" and secondChildType == "TYPE_STRING":
            return (str(evaluate), "TYPE_STRING")

        return (int(evaluate), "TYPE_INT")


# Deals with Logical operations,
# must have two children
class LogicalOp(Node):
    def Evaluate(self):
        firstChildValue, firstChildType = self.children[0].Evaluate()
        secondChildValue, secondChildType = self.children[1].Evaluate()

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

        firstChildValue = bool(firstChildValue)
        secondChildValue = bool(secondChildValue)

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

        return (int(evaluate), "TYPE_BOOL")


# Deals with unary operations,
# must have one child
class UnOp(Node):
    def Evaluate(self):
        childValue, childType = self.children[0].Evaluate()

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
    def Evaluate(self):
        return (int(self.value), "TYPE_INT")


# Returns its own bool value, it's a "boolean" node
class BoolVal(Node):
    def Evaluate(self):
        return (int(self.value == "true"), "TYPE_BOOL")


# Returns its own string value, it's a "string" node
class StringVal(Node):
    def Evaluate(self):
        return (str(self.value), "TYPE_STRING")


# no operation
class NoOp(Node):
    def Evaluate(self):
        return super().Evaluate()


# Assigns an identifier (received by self.value/initValue)
# to it's actual value (self.children[0].Evaluate());
# Sets an Identfier's value on the Symbol Table
class Assign(Node):
    def Evaluate(self):
        if symbolTable.contains(self.value):
            var_type = symbolTable.getType(self.value)
            childValue, _ = self.children[0].Evaluate()
            if var_type == "TYPE_BOOL":
                symbolTable.set(self.value, (int(bool(childValue)), var_type))
            elif var_type == "TYPE_INT":
                symbolTable.set(self.value, (int(childValue), var_type))
            elif var_type == "TYPE_STRING":
                symbolTable.set(self.value, (str(childValue), var_type))
            else:
                raise ValueError("Unkown type.")
        else:
            raise ValueError(f"Set on undeclared variable {self.value}")


# Contary to the Assign object, Identifier used to get
# an identifier's value from the Symbol Table
class Identifier(Node):
    def Evaluate(self):
        # ST is responsible for returning variable value and type
        return symbolTable.get(self.value)


class Declare(Node):
    def Evaluate(self):
        symbolTable.set(self.value, self.children[0])


class While(Node):
    def Evaluate(self):
        # conditional child
        while self.children[0].Evaluate():
            # block or command child
            self.children[1].Evaluate()


class If(Node):
    def Evaluate(self):
        if self.children[0].Evaluate():
            # block or command child 1
            self.children[1].Evaluate()
        else:
            # block or command child 2
            self.children[2].Evaluate()


# prints a value
# composed by identifiers and/or expressions
class Print(Node):
    def Evaluate(self):
        childValue, childType = self.children[0].Evaluate()
        if childType == "TYPE_BOOL":
            if childValue == 1:
                print("true")
            else:
                print("false")
        elif childType == "TYPE_INT":
            print(childValue)
        elif childType == "TYPE_STRING":
            print(childValue.replace('"', ""))


# receives an user input
# Value and Children are not needed
class Read(Node):
    def Evaluate(self):
        return (int(input()), "TYPE_INT")


# A Block can have many instructions. Each line of code
# (instruction) is added as a child of block.
# When each child is evaluated, Assigns and Identifiers are
# being used to build the symbol table and eventualy
# Print a result
class Block(Node):
    def Evaluate(self):
        [i.Evaluate() for i in self.children]
