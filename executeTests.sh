#!/bin/bash
R=(
'0
7
1
1
18
2
6
3
6
4'  #00
'33
4'  #01
''              #02
''              #03
'18'            #04
'Traceback()'   #05
'12'            #06
'3
9
4'  #07
'Traceback()'   #08
''              #09
'Traceback()'   #10
'Traceback()'   #11
'Traceback()'   #12 
'Traceback()'   #13
'Traceback()'   #14
'8'             #15
'2'             #16
'Traceback()'   #17
'2'             #18
'Traceback()'   #19
'2'             #20
''              #21
'Traceback()'   #22
'1
2
3
4
5'  #23
'0'             #24
'1'             #25
'8'             #26
'9
1
0
0
0
0
0'  #27
'1
0
0
0
0
1
2
3'  #28
'13'            #29
'Traceback()'   #30
'15'            #31
'8'             #32 
'12'            #33 
)
files=(./tests/test*.c)
N_tests=${#R[@]}

for (( i=0; i<$N_tests; i++));
do
    A=$(python3 main.py ${files[$i]} 2>&1)
    if ! [[ $A == ${R[$i]} ]]; then # if not equal to number in list
        if ! [[ $A =~ ^${R[$i]}  ]]; then # if regex doesn't match
            echo "Failure on ${files[$i]}. Expected ${R[$i]}, but got $A." 
            exit; 
        fi
    fi
done

echo "All tests passed"