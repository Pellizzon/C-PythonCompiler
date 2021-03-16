# Projeto Compilador

## Lógica da Computação, 7°Semestre, INSPER 2021.1

## v1.1.X

```python main.py '1+2'``` 

```python main.py '789 +345 - 123'```

```python main.py '4/2+3'```

```python main.py '2 + 3 * 5'```

```python main.py '2 + 3 * 3 /*aaaaaaaaaaa*/+ 4'```

```python main.py '2 + 3 * 3 /*aaaaaaaaaaa*/*/+ 4'```

### Diagrama Sintático   

<p align="center">
    <img src="DiagramaSintatico.png">
</p>

### EBNF

<p align="center">
    <img src="EBNF.png" width="40%">
</p>

```EXPRESSION = TERM, {("+" | "-"), TERM} ;```

```TERM = NUMBER, {("*" | "/"), NUMBER} ;```

```NUMBER = DIGIT, {DIGIT} ;```

```DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;```
