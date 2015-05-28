#!/bin/bash

for (( i=0; i<3; i++))
do
    for (( j=2; j<4; j++))
    do
        echo QUALITY $(($i*2+90))
        echo LENGTH $(($j*200+400))
        python3 scaffolding_only_repeats.py $(($j*200+400)) $(($i*2+90))
    done
done
