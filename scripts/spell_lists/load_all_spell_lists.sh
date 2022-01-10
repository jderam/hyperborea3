#!/bin/bash

for F in $(ls -1 *.txt);
do
    echo $F
    python spell_list_inserts.py $F
    echo
done
