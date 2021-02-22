import sys


def resolve_operacao(string):

    string = string.replace(" ", "")
    numbers = []
    symbols = []

    for i in range(len(string)):
        if string[i] == "+" or string[i] == "-":
            if (string[i - 1] == "+" or string[i - 1] == "-") or (
                string[i + 1] == "+" or string[i + 1] == "-"
            ):
                print("Erro: sintaxe inválida")
                return

            symbols.append(string[i])
            string = string[:i] + " " + string[i + 1 :]

    numbers = [int(i) for i in string.strip().split(" ")]

    if len(numbers) == len(symbols):
        if symbols[0] == "+":
            resultado = numbers[0]
        elif symbols[0] == "-":
            resultado = -numbers[0]
        del symbols[0]
    else:
        resultado = numbers[0]
    for j in range(1, len(numbers)):
        if symbols[j - 1] == "+":
            resultado += numbers[j]
        if symbols[j - 1] == "-":
            resultado -= numbers[j]

    print(resultado)


if __name__ == "__main__":

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])

    for i in args:
        resolve_operacao(i)
