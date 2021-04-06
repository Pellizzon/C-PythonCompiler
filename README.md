# Projeto Compilador

## Lógica da Computação, 7°Semestre, INSPER 2021.1

## v2.0.0

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
