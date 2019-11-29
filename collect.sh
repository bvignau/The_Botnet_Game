#!/bin/bash

base_dir=`pwd`
principal="$base_dir/$2.csv"
for ((i = 0 ; i < $1 ; i++)); do 
    size=`wc -l "./simulation_$i/The_BotGame/$20-a.csv" | cut -d" " -f1`
    echo "size = $size" 
    let size--
    tail -n $size "./simulation_$i/The_BotGame/$20-a.csv" >> $principal
done
