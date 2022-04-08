<img src="https://github.com/deepraj1729/Docker-Monitor/blob/main/media/docker.png" class="img-responsive" alt="">

# Docker-Monitor
- Check Docker running status
- Check Container status
- Check Container health status
- Check Application status
- Check Disk Quota status (If disk used >= 80% then notify)
- Notify via email (via SendGrid API)

## Requirements
- Git
- OS running Linux (or WSL for Windows Users), MacOS
- Sendgrid API KEY

## Configure API KEY
Add the sendgrid API key in `docker_monitor/credentials.py`
        
        SEND_GRID_API_KEY = "ENTER_SENDGRID_API_KEY"
        

## Health Check
Add the Health Check Command in the Dockerfile consisting an application

For example running a node js application using docker,
Add this in Dockerfile:

        HEALTHCHECK --interval=20s --timeout=5s \
        CMD npm run start || exit 1

## Run Command:
Entrypoint: 
    
    main.py
    
    
Using Bash:

- Configure the changes in `monitor.sh`
        
        #!/bin/bash

        WORKING_DIR="docker-monitor"
        CONTAINER_NAME="enter_container_name_or_id"
        IP="127.0.0.1"
        PORT=8080
        DISK="/"
        FROM="sender@email"
        TO=("reciever@email1" "reciever@email2" "reciever@email3")

- Then run
    
        bash monitor.sh
    
Using Conda:
- First Setup conda on the VM or locally using `conda-install.sh`
        
        #!/bin/bash

        cd ~/
        mkdir downloads/
        cd downloads/
        wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
        ./Miniconda3-py39_4.11.0-Linux-x86_64.sh

        #Now logout and sign in (incase of remote VM just reconnect using ssh again)
        ############################################################################
        #Later run these commands
        #python -V
        #conda create -n ENV_NAME python=3.8
        #conda activate ENV_NAME
        #cd docker-monitor/
        #pip install -r requirements.txt
        
        
- Now run 
        
        python main.py -n CONTAINER_NAME -ip IP -port PORT -disk "/" -from FROM -to TO

## Run in Remote VMs
This project is specifically designed to run on remote VMs and switch between VMs
using the `vm-ssh-script.sh`

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

## Run this as a CronJob:
Edit the `crontab` file and add the path to the `monitor.sh` file to run the script periodically
        
        crontab -e

Inside the file edit these lines:

        #Runs the monitor.sh every 30mins and saves the logs in case of error
        */30 * * * * /.../monitor.sh >> /.../monitor.log 2>&1
        
        
## CLI Flags:
Usage:

    $ python main.py -h
    usage: main.py [-h] [-v] -n N -ip IP -port PORT -disk DISK -from_ FROM_ -to_ TO_ [TO_ ...]

    Docker-Monitor: A script to monitor your docker containers runinng in different VMs

    optional arguments:
    -h, --help          show this help message and exit
    -v                  show program's version number and exit
    -n N                Pass the Container NAME/ID
    -ip IP              Pass the local IP (e.g: 127.0.0.1) of the VM
    -port PORT          Pass the PORT number where the docker app is exposed (e.g 8080)
    -disk DISK          Pass the disk mount path to check for disk quota stats (e.g. '/')
    -from_ FROM_        Sender Mail (Required for sending notifications for the Container status)
    -to_ TO_ [TO_ ...]  Pass the receiver mail id/ids (will be taken as a list)

