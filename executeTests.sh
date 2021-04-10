#!/bin/bash
R=(
    '6'             #00
    'Traceback()'   #01
    ''              #02
    ''              #03
    '18'            #04
    'Traceback()'   #05
    '12'            #06
    '3
9
4'
    'Traceback()'   #08
    ''              #09
    'Traceback()'   #10
    'Traceback()'   #11
    'Traceback()'   #12 
    'Traceback()'   #13
    )
files=(./tests/*)
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