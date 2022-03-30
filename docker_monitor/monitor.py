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
        self.docker_status = None

        #Container flags
        self.container_name = None
        self.container_obj = None
        self.container_status = None
        self.container_health_status = None

        #application flags
        self.application_url = None
        self.application_status_code = None
        self.application_status = None

        #disk quota flag
        self.disk_mount_path = None
        self.disk_quota_threshold = 80
        self.disk_quota_total = 0
        self.disk_quota_used = 0
        self.disk_quota_free = 0
        self.disk_quota_status = None

        #logs
        now = datetime.now()
        time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
        self.logs_time_stamp = f"\n[ {time_stamp} ]"

        #mail flags
        self.from_ = None
        self.to_ = None
        
    

    """Docker Status Flag"""
    def getDockerStatus(self):
        try:
            self.docker_client = docker.from_env()
            return "running"

        except Exception as e:
            return "not running"



    """Container Status Flag"""
    def getContainerStatus(self):
        try:
            self.container_obj = self.docker_client.containers.get(self.container_name)
            self.container = Container(self.container_obj)

            if self.container.CONTAINER_STATUS != "running" or self.container.HEALTH_STATUS == "unhealthy":
                self.container.getInfo()
            return self.container.CONTAINER_STATUS,self.container.HEALTH_STATUS

        except docker.errors.NotFound as exc:
            self.notify(
                subject="Docker monitoring result! Status: WARNING!!!",
                body="Caution!!! Container not found with the given name"
            )
            print(self.logs_time_stamp)
            print(f"        Check container Name or ID!\n{exc.explanation}")
            return "not running"
    
    

    def getApplicationStatus(self):
        res = req.get(self.application_url)
        try:
            if res.status_code >=200 and res.status_code <=299:
                return "healthy",res.status_code
            else:
                print(self.logs_time_stamp)
                print("     Application Status: unhealthy")
                return "unhealthy",res.status_code

        except Exception as e:
            print(self.logs_time_stamp)
            print(f"    {e}")
            return "unhealthy",404

        

    def getDiskQuotaStatus(self):
        total,used,free = shutil.disk_usage(self.disk_mount_path)
        used_percent = (float(used)/total)*100

        self.disk_quota_used = "{} GB".format(used // (2**30))
        self.disk_quota_free = "{} GB".format(free //(2**30))
        self.disk_quota_total = "{} GB".format(total //(2**30))

        #if used_up space > 80% then throw logs and send warning
        if used_percent >= self.disk_quota_threshold:
            print(self.logs_time_stamp)
            print("     Disk Quota Total: %s" % (self.disk_quota_total))
            print("     Disk Quota Used: %s" % (self.disk_quota_used))
            print("     Disk Quota Free: %s" % (self.disk_quota_free))
            return "warning"
        else:
            return "healthy"

    def notify(self,subject,body):
        email = SendGridEmail(self.from_,self.to_,subject,body)
        email.send()
    
    def convertJSON(self):
        now = datetime.now()
        time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
        data = {"name": self.container.NAME,
                "id": self.container.ID,
                "time_stamp": f"{time_stamp}",
                "docker_status":self.docker_status,
                "container_status": self.container_status,
                "health_status":self.container_health_status,
                "application_status": self.application_status,
                "application_status_code":str(self.application_status_code),
                "disk_quota_status":self.disk_quota_status,
                "disk_quota_used":self.disk_quota_used,
                "disk_quota_free":self.disk_quota_free}
        return data
    


    #Entry point of the class
    """Checks/monitors a particular container"""
    def run(self,container_name,application_url,disk_mount_path,from_,to_):
        self.container_name = container_name
        self.application_url = application_url
        self.disk_mount_path = disk_mount_path
        self.from_ = from_  
        self.to_ = to_ 

        #Get Docker Status
        self.docker_status = self.getDockerStatus()

        #Get Container and Health Status
        self.container_status,self.container_health_status =  self.getContainerStatus()

        #Get application Status
        self.application_status,self.application_status_code = self.getApplicationStatus()

        #Get Disk Quota
        self.disk_quota_status = self.getDiskQuotaStatus()
        
        #JSON body
        json_body = json.dumps(self.convertJSON(),indent=6)

        if self.docker_status != "running" or self.container_status != "running" or self.container_health_status == "unhealthy" or self.application_status == "unhealthy" or self.disk_quota_status == "warning":
            print(f"    JSON: \n        {json_body}")
            print("     MESSAGE: Found some issues")
            self.notify(
                subject="Docker monitoring result! Status: WARNING!!!",
                body = json_body
            )
        else:
            exit()



