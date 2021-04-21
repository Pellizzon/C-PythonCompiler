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
        firstChildEval = self.children[0].Evaluate()
        secondChildEval = self.children[1].Evaluate()

        if self.value == "PLUS":
            evaluate = firstChildEval + secondChildEval
        elif self.value == "MINUS":
            evaluate = firstChildEval - secondChildEval
        elif self.value == "DIV":
            evaluate = firstChildEval / secondChildEval
        elif self.value == "MULT":
            evaluate = firstChildEval * secondChildEval
        else:
            raise ValueError("Could not evaluate BinOp")

        return int(evaluate)


# Deals with unary operations,
# must have one child
class UnOp(Node):
    def Evaluate(self):
        childEval = self.children[0].Evaluate()

        if self.value == "PLUS":
            evaluate = +childEval
        elif self.value == "MINUS":
            evaluate = -childEval
        else:
            raise ValueError("Could not evaluate UnOp")

        return int(evaluate)


# Returns its own value, it's a "number" node
class IntVal(Node):
    def Evaluate(self):
        return int(self.value)


# no operation
class NoOp(Node):
    def Evaluate(self):
        return super().Evaluate()


# Assigns an identifier (received by self.value/initValue)
# to it's actual value (self.children[0].Evaluate());
# Sets an Identfier's value on the Symbol Table
class Assign(Node):
    def Evaluate(self):
        symbolTable.set(self.value, self.children[0].Evaluate())


# Contary to the Assign object, Identifier used to get
# an identifier's value from the Symbol Table
class Identifier(Node):
    def Evaluate(self):
        return symbolTable.get(self.value)


# prints a value
# composed by identifiers and/or expressions
class Print(Node):
    def Evaluate(self):
        print(self.children[0].Evaluate())


# A Block can have many instructions. Each line of code
# (instruction) is added as a child of block.
# When each child is evaluated, Assigns and Identifiers are
# being used to build the symbol table and eventualy
# Print a result
class Block(Node):
    def Evaluate(self):
        [i.Evaluate() for i in self.children]
