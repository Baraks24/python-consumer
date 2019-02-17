#!/bin/bash

python_consumer(){
    python3 python-consumer.py 
}

until python_consumer; do
    echo "'python-consumer.py' crashed with exit code $?. Restarting..." >&2
    sleep 3
done