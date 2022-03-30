# Docker-Monitor
- Check Docker running status
- Check Container status
- Check Container health status
- Check Application status
- Check Disk Quota status (If disk used >= 80% then notify)
- Notify via email (via SendGrid API)


Entrypoint: 
    
    -- main.py

## Add Health Check command inside your Dockerfile for checking Health Status
For example running a node js application:

Add this in Dockerfile:

        HEALTHCHECK --interval=20s --timeout=5s \
        CMD npm run start || exit 1

## Run Command:
Using Bash:

    bash monitor.sh
    
Using Conda:

    python main.py -n CONTAINER_NAME -ip IP -port PORT -disk "/" -from FROM -to TO

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
