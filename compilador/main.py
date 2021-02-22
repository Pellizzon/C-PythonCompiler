import sys

def resolve_operacao(string):

    string = string.replace(' ', '')
    numbers = []
    symbols = []
    
    for i in range(len(string)):
        if string[i] == '+' or string[i] == '-':
            symbols.append(string[i])
            string = string[:i] + ' ' + string[i+1:] 

    numbers = [int(i) for i in string.split(' ')]
    
    resultado = numbers[0]

    for j in range(1, len(numbers)):
        # print(j)
        if symbols[j-1] == '+':
            resultado += numbers[j]
        if symbols[j-1] == '-':
            resultado -= numbers[j]

    print(resultado)


if __name__ == "__main__":

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])

    for i in args:
        resolve_operacao(i)

           


