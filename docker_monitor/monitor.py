from docker_monitor.container import Container
from docker_monitor.notify import SendGridEmail
import docker
import requests as req
import json
from datetime import datetime
import shutil



class DockerMonitor:
    """Initial Initialization"""
    def __init__(self):
        #docker flags
        self.docker_client = None

        #Container flags
        self.container_name = None
        self.container_obj = None

        #application flags
        self.application_url = None

        #disk quota flag
        self.disk_mount_path = None
        self.disk_quota_threshold = 80
        self.disk_quota_total = 0
        self.disk_quota_used = 0
        self.disk_quota_free = 0
        self.disk_quota_status = None

        #logs
        self.logger = {}
        now = datetime.now()
        time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
        self.logs_time_stamp = f"\n[ {time_stamp} ]"
        self.logger["TIME_STAMP"] = str(time_stamp)

        #mail flags
        self.from_ = None
        self.to_ = None

        
    

    """Docker Status Flag"""
    def getDockerStatus(self):
        try:
            self.docker_client = docker.from_env()
            self.logger["DOCKER_STATUS"] = "RUNNING"

        except Exception as e:
            #Set Msg
            self.logger["MESSAGE"] = "Docker Not Running!!! Check into VM ASAP"

            #Set Flags
            self.logger["DOCKER_STATUS"] = "NOT RUNNING"
            
            
            #Console Logs
            print(self.logs_time_stamp)
            print("     MESSAGE: Found some issues")
            print("     {}".format(self.logger["MESSAGE"]))
            print("     JSON: "+json.dumps(self.logger,indent=6))

            #Send Mail
            self.notify(
                subject=self.logger["MESSAGE"],
                body=json.dumps(self.logger,indent=6)
            )

            #End the program
            exit()



    """Container Status Flag"""
    def getContainerStatus(self):
        try:
            #Search for the Container
            self.container_obj = self.docker_client.containers.get(self.container_name)

            #Set as Container object
            self.container = Container(self.container_obj)

            #Set Flags
            self.logger["CONTAINER_NAME"] = self.container.NAME
            self.logger["CONTAINER_ID"] = self.container.ID
            self.logger["CONTAINER_STATUS"] = self.container.CONTAINER_STATUS.upper()
            self.logger["CONTAINER_HEALTH_STATUS"] = self.container.HEALTH_STATUS.upper()

            if self.logger["CONTAINER_STATUS"] != "RUNNING" or self.logger["CONTAINER_HEALTH_STATUS"] == "UNHEALTHY" or self.logger["CONTAINER_HEALTH_STATUS"] == "UNAVAILABLE":
                #Set Msg
                self.logger["MESSAGE"] = f"{self.container_name} Container Status Unhealthy!!! Check your container ASAP"

                #Console Logs
                print(self.logs_time_stamp)
                print("     MESSAGE: Found some issues")
                print("     {}".format(self.logger["MESSAGE"]))
                print("     JSON: "+json.dumps(self.logger,indent=6))

                #Send Mail
                self.notify(
                    subject=self.logger["MESSAGE"],
                    body=json.dumps(self.logger,indent=6)
                )

                #End the program
                exit()

        
        except docker.errors.NotFound as exc:
            #Set flags
            self.logger["CONTAINER_STATUS"] = "NOT RUNNING"

            #Set Msg
            self.logger["MESSAGE"] = f"{self.container_name} Container Not Running!!! Check into VM ASAP"

            #Console logs
            print(self.logs_time_stamp)
            print("     MESSAGE: Found some issues")
            print("     {}".format(self.logger["MESSAGE"]))
            print(f"     {exc.explanation}")
            print("     JSON: "+json.dumps(self.logger,indent=6))

            #Send Mail
            self.notify(
                subject=self.logger["MESSAGE"],
                body=json.dumps(self.logger,indent=6)
            )

            #End the program
            exit()

            
    
    
    """Application Status Flag"""
    def getApplicationStatus(self):
        res = req.get(self.application_url)
        try:
            if res.status_code >=200 and res.status_code <=299:
                self.logger["APPLICATION_STATUS"] = "HEALTHY"
                self.logger["APPLICATION_STATUS_CODE"] = str(res.status_code)
                
            else:
                #Set Status flags
                self.logger["APPLICATION_STATUS"] = "UNHEALTHY"
                self.logger["APPLICATION_STATUS_CODE"] = str(res.status_code)

                #Set Msg
                self.logger["MESSAGE"] = f"Application Error!!! Status code {res.status_code} Check it ASAP"

                #Console Logs
                print(self.logs_time_stamp)
                print("     MESSAGE: Found some issues")
                print("     {}".format(self.logger["MESSAGE"]))
                print("     JSON: "+json.dumps(self.logger,indent=6))

                #Send Mail
                self.notify(
                    subject=self.logger["MESSAGE"],
                    body=json.dumps(self.logger,indent=6)
                )

                #End the program
                exit()


        except Exception as e:
            #Set Status flags
            self.logger["APPLICATION_STATUS"] = "UNHEALTHY"

            #Set Msg
            self.logger["MESSAGE"] = f"Application Error!!! Status code {res.status_code}"

            #Console Logs
            print(self.logs_time_stamp)
            print("     MESSAGE: Found some issues")
            print("     {}".format(self.logger["MESSAGE"]))
            print("     JSON: "+json.dumps(self.logger,indent=6))

            #Send Mail
            self.notify(
                subject=self.logger["MESSAGE"],
                body=json.dumps(self.logger,indent=6)
            )

            #End the program
            exit()

        
    """Disk-Quota Status Flag"""
    def getDiskQuotaStatus(self):
        total,used,free = shutil.disk_usage(self.disk_mount_path)
        used_percent = (float(used)/total)*100

        self.disk_quota_used = "{} GB".format(used // (2**30))
        self.disk_quota_free = "{} GB".format(free //(2**30))
        self.disk_quota_total = "{} GB".format(total //(2**30))

        #if used_up space > 80% then throw logs and send warning
        if used_percent >= self.disk_quota_threshold:
            #set status flag
            self.logger["DISK_QUOTA_STATUS"] = "UNHEALTHY"
            self.logger["DISK_QUOTA_USED"] = f"{self.disk_quota_used}"
            self.logger["DISK_QUOTA_FREE"] =  f"{self.disk_quota_free}"
            self.logger["DISK_QUOTA_TOTAL"] =  f"{self.disk_quota_total}"

            #Set Msg
            self.logger["MESSAGE"] = "VM Running out of space (>80% space consumed) !!! Check it ASAP"

            print(self.logs_time_stamp)
            print("     MESSAGE: Found some issues")
            print("     {}".format(self.logger["MESSAGE"]))
            print("     JSON: "+json.dumps(self.logger,indent=6))

            #Send Mail
            self.notify(
                subject=self.logger["MESSAGE"],
                body=json.dumps(self.logger,indent=6)
            )

            #End the program
            exit()
            
        else:
            self.logger["DISK_QUOTA_STATUS"] = "HEALTHY"
            self.logger["DISK_QUOTA_USED"] = f"{self.disk_quota_used}"
            self.logger["DISK_QUOTA_FREE"] =  f"{self.disk_quota_free}"
            self.logger["DISK_QUOTA_TOTAL"] =  f"{self.disk_quota_total}"
            

    def notify(self,subject,body):
        email = SendGridEmail(self.from_,self.to_,subject,body)
        email.send()
    

    #Entry point of the class
    """Checks/monitors a particular container"""
    def run(self,container_name,application_url,disk_mount_path,from_,to_):
        self.container_name = container_name
        self.application_url = application_url
        self.disk_mount_path = disk_mount_path
        self.from_ = from_  
        self.to_ = to_ 

        #Get Docker Status
        self.getDockerStatus()

        #Get Container and Health Status
        self.getContainerStatus()

        #Get application Status
        self.getApplicationStatus()

        #Get Disk Quota
        self.getDiskQuotaStatus()