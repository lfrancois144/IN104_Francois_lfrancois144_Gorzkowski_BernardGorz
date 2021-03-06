#!/bin/bash

nb=$*
avg=$*
max=$*
avg=0
max=0

if [ -z "$nb" ]; then
    nb=100
fi

for i in $(seq 1 $nb); do
    score=$(hanabi --ai=Random |grep score |sed -e 's/.*is //')
    let "avg+=$score"
    if [ $max -lt $score ]; then
        max=$score
    fi
done
let "avg=$avg/$nb"

echo avg=$avg
echo max=$max
