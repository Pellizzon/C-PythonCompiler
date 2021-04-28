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


# Deals with Logical operations,
# must have two children
class LogicalOp(Node):
    def Evaluate(self):
        firstChildEval = self.children[0].Evaluate()
        secondChildEval = self.children[1].Evaluate()

        if self.value == "LESSTHAN":
            evaluate = firstChildEval < secondChildEval
        elif self.value == "BIGGERTHAN":
            evaluate = firstChildEval > secondChildEval
        elif self.value == "EQOP":
            evaluate = firstChildEval == secondChildEval
        elif self.value == "AND":
            evaluate = firstChildEval and secondChildEval
        elif self.value == "OR":
            evaluate = firstChildEval or secondChildEval
        else:
            raise ValueError("Could not evaluate LogicalOp")

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
        elif self.value == "NOT":
            evaluate = not childEval
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


class While(Node):
    def Evaluate(self):
        # conditional child
        while self.children[0].Evaluate():
            # block or command child
            self.children[1].Evaluate()


class If(Node):
    def Evaluate(self):
        # conditional child
        if len(self.children) == 2:
            if self.children[0].Evaluate():
                # block or command child 1
                self.children[1].Evaluate()
            else:
                pass
        else:
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
        print(self.children[0].Evaluate())


# receives an user input
# Value and Children are not needed
class Read(Node):
    def Evaluate(self):
        return int(input("Insert a number: "))


# A Block can have many instructions. Each line of code
# (instruction) is added as a child of block.
# When each child is evaluated, Assigns and Identifiers are
# being used to build the symbol table and eventualy
# Print a result
class Block(Node):
    def Evaluate(self):
        [i.Evaluate() for i in self.children]
