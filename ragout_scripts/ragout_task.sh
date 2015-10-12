#!/bin/bash

for (( i=0; i<6; i++))
do
    echo QUALITY $(($i*2+90))
    for (( j=0; j<14; j++))
    do
        python3 ragout_prepare_data.py $(($j*200+400)) $(($i*2+90))
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-chimp/ragout/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-chimp/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/5-chimp/ragout/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/5-chimp/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-human/ragout/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-human/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/5-human/ragout/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/5-human/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-human/ragout/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-human/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/4-human/ragout/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/4-human/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-chimp/ragout/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-chimp/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/4-chimp/ragout/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/4-chimp/ragout/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/human/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/human/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/chimp/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/chimp/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/rat/vertebrate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-3/ragout/rat/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/human/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/human/out
	    #run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/chimp/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/chimp/out
	    run-ragout /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/gorilla/primate.cfg --outdir /home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/gorilla/out
        python3 get_ragout_history.py $(($j*200+400)) $(($i*2+90))
    done
done
python3 ragout_evaluation.py
