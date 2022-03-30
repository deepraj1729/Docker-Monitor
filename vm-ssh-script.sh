#!/bin/bash

WORKING_DIR="docker-monitor"
CONTAINER_NAME="enter_container_name_or_id"
IP="127.0.0.1"
PORT=8080
DISK="/"
FROM="sender@email"
TO=("reciever@email1" "reciever@email2" "reciever@email3")

#Switch between VMs using SSH and execute docker-monitoring script
eval `ssh-agent` > /dev/null
ssh-add ~/.ssh/ssh-key >/dev/null 2>&1

ssh host@ip bash -l << ENDSSH
    source ~/miniconda3/bin/activate docker-monitor
    cd ${WORKING_DIR}
    python main.py -n "${CONTAINER_NAME}" -ip "${IP}" -port ${PORT} -disk "/" -from "${FROM}" -to ${TO[@]}
ENDSSH
##############################################  EOF  #####################################################