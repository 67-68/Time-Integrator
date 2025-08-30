class INV_ServiceContainer:
    def __init__(self):
        self._services = {}
        
    def add_service(self,name,service):
        self._services[name] = service
        
    def getService(self,name):
        return self._services[name]