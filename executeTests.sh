#!/bin/bash
R=(
    '6' 
    'Traceback()' 
    '' 
    '' 
    '18' 
    'Traceback()' 
    '12' 
    '3
9
4'
    ''
    ''
    '' 
    '' 
    '' 
    '' 
    '' 
    '')
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