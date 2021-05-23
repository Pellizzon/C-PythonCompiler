# Projeto Compilador

## Lógica da Computação, 7°Semestre, INSPER 2021.1

## Status:
![git status](http://3.129.230.99/svg/Pellizzon/LogicaDaComputacao/)

## v3.0

### Diagrama Sintático   

<p align="center">
    <img src="DS.png">
</p>

### EBNF

<p align="center">
    <img src="EBNF.png" width="40%">
</p>

```
BLOCK = "{", { COMMAND, } "}" ;
COMMAND = ( λ | ASSIGNMENT | PRINT ), ";" | BLOCK | WHILESTMT | IFSMT | DECLARE ;
ASSIGNMENT = IDENTIFIER, "=", OREXPR ;
PRINT = "println", "(", OREXPR, ")" ;
DECLARE = TYPE, IDENTIFIER, ";" ;

TYPE = ( "int" | "bool" ) ;

IFSTMT = "if", "(", OREXPR, ")", COMMAND ["else", COMMAND] ;
WHILESTMT = "while", "(", OREXPR, ")", COMMAND ;

OREXPR = ANDEXPR ["||", ANDEXPR] ;
ANDEXPR = EQEXPR ["&&", EQEXPR] ;
EQEXPR = RELEXPR ["==", EQEXPR] ;
RELEXPR = EXPRESSION [(">" | "<"), EXPRESSION] ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"| "!"), FACTOR) | NUMBER | "(", OREXPR, ")" | IDENTIFIER | READ | STRING | BOOL ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
BOOL = (true | false) ;
```
