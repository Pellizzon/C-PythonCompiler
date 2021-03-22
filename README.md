# Projeto Compilador

## Lógica da Computação, 7°Semestre, INSPER 2021.1

## v1.2.X

Sem erros:

> python main.py '(3 + 2) /5'

> python main.py '--77'

> python main.py '+--++3'

> python main.py '3 - -2/4'

> python main.py '4/(1+1)*2'

Com erros:

> python main.py '(2*2'

> python main.py '(3-(8)'

> python main.py '3+2)'


### Diagrama Sintático   

<p align="center">
    <img src="DiagramaSintatico.png">
</p>

### EBNF

<p align="center">
    <img src="EBNF.png" width="40%">
</p>

```EXPRESSION = TERM, { ("+" | "-"), TERM } ;```

```TERM = FACTOR, { ("*" | "/"), FACTOR } ;```

```FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER ;```

```NUMBER = DIGIT, {DIGIT} ;```

```DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;```
