from docker_monitor.monitor import DockerMonitor
import argparse

VERSION="1.0.1"

def main():
    parser = argparse.ArgumentParser(description="Docker-Monitor: A script to monitor your docker containers runinng in different VMs")

    #Version
    parser.add_argument('-v', action='version', version=VERSION)

    #Container name
    parser.add_argument('-n', type = str,help = "Pass the Container NAME/ID", required=True)

    #hostip
    parser.add_argument('-ip',type = str,help = "Pass the local IP (e.g: 127.0.0.1) of the VM", required=True)

    #port
    parser.add_argument('-port',type =int,help = "Pass the PORT number where the docker app is exposed (e.g 8080)", required=True)


    #disk quota check mount path
    parser.add_argument('-disk',type =str,help = "Pass the disk mount path to check for disk quota stats (e.g. '/')", required=True)

    #mail from
    parser.add_argument('-from_',type = str,help = "Sender Mail (Required for sending notifications for the Container status)", required=True)

    #mail to [list]
    parser.add_argument('-to_',type = str,nargs='+',help = "Pass the receiver mail id/ids (will be taken as a list)", required=True)



    try:
        args = parser.parse_args()

        CONTAINER_NAME = args.n
        HOST_IP = args.ip
        PORT = args.port
        DISK_CHECK_PATH = args.disk 
        FROM_ = args.from_
        TO_ = args.to_
        APPLICATION_URL = f"http://{HOST_IP}:{PORT}/"

        mnt = DockerMonitor()
        mnt.run(CONTAINER_NAME,APPLICATION_URL,DISK_CHECK_PATH,FROM_,TO_)

    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()