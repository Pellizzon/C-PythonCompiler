import sys
from components.symbolTable import SymbolTable
from components.parser import Parser
from components.assembler import asm


if __name__ == "__main__":

    if not sys.argv[1].endswith(".c"):
        raise ValueError("Input file must have '.c' extension")

    with open(f"{sys.argv[1]}", "r") as f:
        inputData = f.read()

    symbolTable = SymbolTable()
    asm.defineHeader()
    Parser().run(inputData).Evaluate(symbolTable)
    asm.defineEnd()
    asm.returnAsm()
