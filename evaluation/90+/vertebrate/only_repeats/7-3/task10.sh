#!/bin/bash

for (( i=3; i<6; i++))
do
    for (( j=1; j<2; j++))
    do
        echo QUALITY $(($i*2+90))
        echo LENGTH $(($j*200+400))
        python3 scaffolding_only_repeats.py $(($j*200+400)) $(($i*2+90))
    done
done
