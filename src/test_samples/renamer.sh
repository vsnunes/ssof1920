#!/bin/bash
i=0
for f in *.py
do
    filename="${f%.*}"
    printf -v j "%02d" $i
    mkdir -p "T07-$j"
    cp $filename.py "T07-$j/program.py"

    if [ -f "$filename.conf" ]; then
        cp $filename.conf "T07-$j/patterns.json"
    else 
        cp simple.conf "T07-$j/patterns.json"
    fi 

    cp $filename.json "T07-$j/input.json"
    cp $filename.out "T07-$j/output.json"
    i=$(($i+1))
done
