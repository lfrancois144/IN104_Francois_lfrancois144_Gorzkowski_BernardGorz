#!/bin/bash

nb=$*
avg=$*
max=$*
min=$*
avg=0
max=0
min=25

if [ -z "$nb" ]; then
    nb=500
fi

for i in $(seq 1 $nb); do
    score=$(./src/hanabi/hanabi --ai=BigBrain |grep score |sed -e 's/.*is //')
    let "avg=$avg+100*$score"
    if [ $max -lt $score ]; then
        max=$score
    fi
    if [ $score -lt $min ]; then
        min=$score
    fi
done
let "avg=$avg/$nb"

echo tests=$nb
echo avg=$avg | sed 's/..$/.&/'
echo max=$max
echo min=$min