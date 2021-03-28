#!/bin/bash
R=('2' '1' '77' '3' '3' '4' '1' '145' '-1' '5' 'err' '49')
N_tests=11

for i in {0..11}
do
    A=$(python3 main.py "./tests/test$i.c" 2>&1)
    if ! [[ $A == ${R[$i]} ]]; then # if not equal to number in list
        if ! [[ $A =~ ValueError ]]; then # if regex doesn't match
            echo "Failure on test$i.c" 
            exit; 
        fi
    fi
done

echo "All tests passed"