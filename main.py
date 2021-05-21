import sys
from components.parser import Parser
from components.assembler import asm

# from components.node import symbolTable

if __name__ == "__main__":

    if not sys.argv[1].endswith(".c"):
        raise ValueError("Input file must have '.c' extension")

    with open(f"{sys.argv[1]}", "r") as f:
        inputData = f.read()

    asm.defineHeader()
    Parser().run(inputData).Evaluate()
    asm.defineEnd()
    asm.returnAsm()
    # print(symbolTable.symbols)
