# Projeto Compilador

## Lógica da Computação, 7°Semestre, INSPER 2021.1

## Status:
![git status](http://3.129.230.99/svg/Pellizzon/LogicaDaComputacao/)

## v2.3

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
COMMAND = ( λ | ASSIGNMENT | PRINT | READ), ";" | BLOCK | WHILESTMT | IFSMT | DECLARE ;
ASSIGNMENT = IDENTIFIER, "=", OREXPR ;
PRINT = "println", "(", OREXPR, ")" ;
READ = "readln", "(", ")" ;
DECLARE = TYPE, IDENTIFIER, ";" ;

TYPE = ( "int" | "strign" | "bool" ) ;


IFSTMT = "if", "(", OREXPR, ")", COMMAND ["else", COMMAND] ;
WHILESTMT = "while", "(", OREXPR, ")", COMMAND ;

OREXPR = ANDEXPR ["||", ANDEXPR] ;
ANDEXPR = EQEXPR ["&&", EQEXPR] ;
EQEXPR = RELEXPR ["==", EQEXPR] ;
RELEXPR = EXPRESSION [(">" | "<"), EXPRESSION] ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"| "!"), FACTOR) | NUMBER | "(", OREXPR, ")" | IDENTIFIER | READ | STRING;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
STRING = QUOT_MARK, {(DIGIT | LETTER | SPECIAL_CHARACTERS)}, QUOT_MARK ;
QUOT_MARK = '"' ;
```
