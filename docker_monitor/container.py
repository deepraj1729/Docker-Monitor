import json
class Container:
    def __init__(self,container_obj):
        self.DEFAULT_HEALTH_STATUS = ["starting","healthy","unhealthy"]
        self.CONTAINER_OBJ = container_obj
        self.NAME = str(self.CONTAINER_OBJ.name)
        self.ID = str(self.CONTAINER_OBJ.id)
        self.ATTRS = self.CONTAINER_OBJ.attrs
        self.CONTAINER_STATUS = str(self.CONTAINER_OBJ.status)
        self.HEALTH_STATUS = ""
        try:
            self.HEALTH_STATUS = str(self.ATTRS["State"]["Health"]["Status"])

        except Exception as e:
            self.HEALTH_STATUS = "UNAVAILABLE"
    
    
    def getContainerAttributes(self,obj_attrs):
        attrs = json.dumps(obj_attrs,indent=6)
        return attrs
