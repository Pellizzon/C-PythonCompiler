from components.symbolTable import SymbolTable
from components.assembler import Assembler
from components.assembler import asm


class NodeID:
    def __init__(self):
        self.id = 0

    def createNodeIdentifier(self):
        newId = self.id
        self.id += 1
        return newId


nodeId = NodeID()


class Node:
    def __init__(self, initValue, initChildren=[]):
        self.value = initValue
        self.children = initChildren
        self.id = nodeId.createNodeIdentifier()

    def Evaluate(self, symbolTable):
        return


# Deals with binary operations,
# must have two children
class BinOp(Node):
    def Evaluate(self, symbolTable):
        self.children[0].Evaluate(symbolTable)
        asm.asm += "PUSH EBX\n"
        self.children[1].Evaluate(symbolTable)
        asm.asm += "POP EAX\n"

        if self.value == "PLUS":
            asm.asm += f"ADD EAX, EBX\n"
        elif self.value == "MINUS":
            asm.asm += f"SUB EAX, EBX\n"
        elif self.value == "DIV":
            asm.asm += f"DIV EBX\n"
        elif self.value == "MULT":
            asm.asm += f"IMUL EBX\n"
        else:
            raise ValueError("Could not evaluate BinOp")

        asm.asm += "MOV EBX, EAX\n"


# Deals with Logical operations,
# must have two children
class LogicalOp(Node):
    def Evaluate(self, symbolTable):
        self.children[0].Evaluate(symbolTable)
        asm.asm += "PUSH EBX\n"
        self.children[1].Evaluate(symbolTable)
        asm.asm += "POP EAX\n"

        if self.value == "LESSTHAN":
            asm.asm += f"CMP EAX, EBX\n"
            asm.asm += f"CALL binop_jl\n"
        elif self.value == "BIGGERTHAN":
            asm.asm += f"CMP EAX, EBX\n"
            asm.asm += f"CALL binop_jg\n"
        elif self.value == "EQOP":
            asm.asm += f"CMP EAX, EBX\n"
            asm.asm += f"CALL binop_je\n"
        elif self.value == "AND":
            asm.asm += f"AND EBX, EAX\n"
        elif self.value == "OR":
            asm.asm += f"OR EBX, EAX\n"
        else:
            raise ValueError("Could not evaluate LogicalOp")


# Deals with unary operations,
# must have one child
class UnOp(Node):
    def Evaluate(self, symbolTable):
        self.children[0].Evaluate(symbolTable)

        if self.value == "PLUS":
            pass
        elif self.value == "MINUS":
            asm.asm += "NEG EBX\n"
        elif self.value == "NOT":
            asm.asm += "NOT EBX\n"
        else:
            raise ValueError("Could not evaluate UnOp")


# Returns its own value, it's a "number" node
class IntVal(Node):
    def Evaluate(self, symbolTable):
        asm.asm += f"MOV EBX, {self.value}\n"


# Returns its own bool value, it's a "boolean" node
class BoolVal(Node):
    def Evaluate(self, symbolTable):
        asm.asm += f"MOV EBX, {int(self.value == 'true')}\n"


# no operation
class NoOp(Node):
    def Evaluate(self, symbolTable):
        asm.asm += "NOP\n"


# Assigns an identifier (received by self.value/initValue)
# to it's actual value (self.children[0].Evaluate(symbolTable));
# Sets an Identfier's value on the Symbol Table
class Assign(Node):
    def Evaluate(self, symbolTable):
        if symbolTable.contains(self.value):
            var_type = symbolTable.getType(self.value)
            self.children[0].Evaluate(symbolTable)
            var_address = symbolTable.getAddress(self.value)
            symbolTable.set(self.value, (var_address, var_type))
            asm.asm += f"MOV [EBP-{var_address}] , EBX\n"
        else:
            raise ValueError(f"Set on undeclared variable '{self.value}'")


# Contary to the Assign object, Identifier used to get
# an identifier's value from the Symbol Table
class Identifier(Node):
    def Evaluate(self, symbolTable):
        # ST is responsible for returning variable value and type
        varAddress, varType = symbolTable.get(self.value)
        asm.asm += f"MOV EBX, [EBP-{varAddress}]\n"
        return symbolTable.get(self.value)


class Declare(Node):
    def Evaluate(self, symbolTable):
        asm.asm += f"PUSH DWORD 0\n"
        symbolTable.declare(self.value, self.children[0])


class While(Node):
    def Evaluate(self, symbolTable):
        asm.asm += f"LOOP_{self.id}:\n"
        # conditional child
        self.children[0].Evaluate(symbolTable)
        asm.asm += f"CMP EBX, False\n"
        asm.asm += f"JE EXIT_{self.id}\n"
        self.children[1].Evaluate(symbolTable)
        asm.asm += f"JMP LOOP_{self.id}\n"
        asm.asm += f"EXIT_{self.id}:\n"


class If(Node):
    def Evaluate(self, symbolTable):
        self.children[0].Evaluate(symbolTable)
        asm.asm += f"CMP EBX, False\n"
        asm.asm += f"JE ELSE_{self.id}\n"
        # block or command child 1
        self.children[1].Evaluate(symbolTable)
        asm.asm += f"JMP IF_EXIT_{self.id}\n"
        asm.asm += f"ELSE_{self.id}:\n"
        # block or command child 2
        self.children[2].Evaluate(symbolTable)
        asm.asm += f"IF_EXIT_{self.id}:\n"


# prints a value
# composed by identifiers and/or expressions
class Print(Node):
    def Evaluate(self, symbolTable):
        self.children[0].Evaluate(symbolTable)

        asm.asm += f"PUSH EBX\nCALL print\nPOP EBX\n"


# A Block can have many instructions. Each line of code
# (instruction) is added as a child of block.
# When each child is evaluated, Assigns and Identifiers are
# being used to build the symbol table and eventualy
# Print a result
class Block(Node):
    def Evaluate(self, symbolTable):
        [i.Evaluate(symbolTable) for i in self.children]
