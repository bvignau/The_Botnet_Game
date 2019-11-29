#!/bin/bash

base_dir=`pwd`
for ((i = 0 ; i < $1 ; i++)); do
    mkdir "simulation_$i"
    ls
    cp -R "The_BotGame" "simulation_$i"
    cd "./simulation_$i/The_BotGame/"
    python ./main.py &
    cd $base_dir
done


