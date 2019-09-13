#!/bin/bash

# this function takes 1 argument ("work" or "personal" for example to change the PERSONAL_DIRECTORY env variable.
# usage: source switch_to.sh work
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
fi
export PERSONAL_DIRECTORY=$1
export TASKDATA=~/core/$PERSONAL_DIRECTORY/task
echo ""
echo "--------> Switched personal directory to: $1"
echo ""