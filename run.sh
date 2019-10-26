#!/usr/bin/env bash

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -s|--size)
    MAP_SIZE="$2"
    shift
    shift
    ;;
    *)
    echo "unknown option ${1}"
    shift
    ;;
esac
done

if [[ -z ${MAP_SIZE} ]]; then
    MAP_SIZE="7x7"
fi


python3.7 main.py --size $MAP_SIZE
python3.7 ${DUCKIE_TOWN_PATH}/manual_control.py --env-name Duckietown-udem1-v0manual --map-name ./maps/new_map.yaml