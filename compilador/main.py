import sys


class Compiler:
    def __init__(self, initString):
        self.string = initString
        self.numbers = []
        self.symbols = []
        self.result = None

    def compile_code(self):
        self.string = self.string.replace(" ", "")

        for i in range(len(self.string)):
            if self.string[i] == "+" or self.string[i] == "-":
                if (self.string[i - 1] == "+" or self.string[i - 1] == "-") or (
                    self.string[i + 1] == "+" or self.string[i + 1] == "-"
                ):
                    print("Erro: sintaxe inválida")
                    return False

                self.symbols.append(self.string[i])
                self.string = self.string[:i] + " " + self.string[i + 1 :]

        self.numbers = [int(i) for i in self.string.strip().split(" ")]
        return True

    def calculate(self):
        if len(self.numbers) == len(self.symbols):
            if self.symbols[0] == "+":
                self.result = self.numbers[0]
            elif self.symbols[0] == "-":
                self.result = -self.numbers[0]
            del self.symbols[0]
        else:
            self.result = self.numbers[0]

        for j in range(1, len(self.numbers)):
            if self.symbols[j - 1] == "+":
                self.result += self.numbers[j]
            if self.symbols[j - 1] == "-":
                self.result -= self.numbers[j]

    def execute(self):
        can_calculate = self.compile_code()
        if can_calculate:
            self.calculate()
            print(self.result)


if __name__ == "__main__":

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])

    for i in args:
        Compiler(i).execute()
