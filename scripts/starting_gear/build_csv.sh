#!/bin/bash

for i in $(seq 26)
do
    sed -e "s/, /\n/g" $i.txt | sed -e "s/^/$i,/g" >> starting_equip.csv
done
