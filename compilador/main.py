import sys
import re


class Compiler:
    def __init__(self, initString):
        self.string = initString
        self.numbers = []
        self.symbols = []
        self.result = 0

    def getNumbers(self):
        self.numbers = [int(i) for i in re.findall(r"\d+", self.string)]
        # print(self.numbers)

    def getSymbols(self):
        self.symbols = re.findall(r"\D", self.string)
        # print(re.findall(r"\D", self.string))

    def checkSymbols(self):
        accepted_symbols = ["+", "-"]
        self.symbols = list(filter(lambda x: x in accepted_symbols, self.symbols))
        # print(self.symbols)

    def insuficientOperands(self):
        if len(self.symbols) <= len(self.numbers) - 2:
            # 3 4 --> 2 numbers 0 symbols
            # 2+4 4 --> 3 numbers 1 symbol
            print("Error: Insufficient operands to perform operation")
            return True
        return False

    def isValidString(self):
        self.string = self.string.replace(" ", "")
        try:
            for i in range(len(self.string)):
                if self.string[i] == "+" or self.string[i] == "-":
                    if self.string[i + 1] == "+" or self.string[i + 1] == "-":
                        print("Error: invalid syntax")
                        return False
        except:
            # example: 10+3+4-
            print("Error: invalid operand position")
            return False

        return True

    def isValidEquation(self):
        if len(self.numbers) > 1:
            return True
        print("Error: cannot calculate equation with one number")
        return False

    def calculate(self):
        if len(self.symbols) != len(self.numbers):
            self.result += self.numbers[0]
        else:
            if self.symbols[0] == "+":
                self.result += self.numbers[0]
            elif self.symbols[0] == "-":
                self.result -= self.numbers[0]
            del self.symbols[0]

        for j in range(1, len(self.numbers)):
            if self.symbols[j - 1] == "+":
                self.result += self.numbers[j]
            if self.symbols[j - 1] == "-":
                self.result -= self.numbers[j]

        print(self.result)

    def execute(self):
        self.getNumbers()
        self.getSymbols()
        self.checkSymbols()
        if (
            self.isValidEquation()
            and not self.insuficientOperands()
            and self.isValidString()
        ):
            self.calculate()


if __name__ == "__main__":

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])

    for i in args:
        Compiler(i).execute()
