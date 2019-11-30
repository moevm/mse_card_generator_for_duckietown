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
    -c|--crossroad_count)
    CROSSROAD_COUNT="$2"
    shift
    shift
    ;;
    -l|--length)
    LENGTH="$2"
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
    MAP_SIZE="9x9"
fi

if [[ -z ${CROSSROAD_COUNT} ]]; then
    CROSSROAD_COUNT="6"
fi

if [[ -z ${LENGTH} ]]; then
    LENGTH="10"
fi


python3.7 main.py --size $MAP_SIZE --crossroad_count $CROSSROAD_COUNT --road_length $LENGTH
python3.7 ${DUCKIE_TOWN_PATH}/manual_control.py --env-name Duckietown-small_loop-v0 --seed 2 --map-name ./maps/new_map.yaml
