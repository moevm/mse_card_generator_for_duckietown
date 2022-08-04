#!/usr/bin/env bash

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -s | --size)
    MAP_SIZE="$2"
    shift
    shift
    ;;
  -c | --crossroad_count)
    CROSSROAD_COUNT="$2"
    shift
    shift
    ;;
  -l | --length)
    LENGTH="$2"
    shift
    shift
    ;;
  -p | --path)
    SAVE_PATH="$2"
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

if [[ -z ${SAVE_PATH} ]]; then
  SAVE_PATH="./maps"
fi

python3 main.py --size $MAP_SIZE --crossroad_count $CROSSROAD_COUNT --road_length $LENGTH --path $SAVE_PATH
