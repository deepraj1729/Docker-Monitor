class Container:
    def __init__(self,container_obj):
        self.DEFAULT_HEALTH_STATUS = ["starting","healthy","unhealthy"]
        self.CONTAINER_OBJ = container_obj
        self.NAME = self.CONTAINER_OBJ.name
        self.ID = self.CONTAINER_OBJ.id
        self.ATTRS = self.CONTAINER_OBJ.attrs
        self.CONTAINER_STATUS = self.CONTAINER_OBJ.status
        self.HEALTH_STATUS = self.ATTRS["State"]["Health"]["Status"]
    
    
    def getContainerAttributes(self,obj_attrs):
        attrs = json.dumps(obj_attrs,indent=6)
        return attrs


    def getInfo(self):
        print("---------------------------------------")
        print("        Docker Container Info")
        print("---------------------------------------")
        print(f"Name: {self.NAME}")
        print(f"ID: {self.ID}")
        print(f"Container Status: {self.CONTAINER_STATUS}")
        print(f"Health Status: {self.HEALTH_STATUS}")
