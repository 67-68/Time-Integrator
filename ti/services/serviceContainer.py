from ti.dataAccess.dataService import DataService
from ti.dataAccess.insightCacheService import InsightCacheService
from ti.dataAccess.insightManager import InsightManager
from ti.engine.insightEngine import InsightEngine


class ServiceContainer:
    def __init__(self):
        """_summary_
        负责创建和保持所有的服务
        """
        self.services = {}
        
        # 现在先不区分"哪一套的"IM, IE
        cache =  InsightCacheService()
        self.services["ICS"] = cache
        
        manager = InsightManager(cache)
        self.services["IM"] = manager
        
        engine = InsightEngine(cache)
        self.services["IE"] = engine
        
        dataService = DataService()
        self.services["DS"] = dataService
            
    def getServices(self):
        """_summary_
        返回一个字典，以下是可用的key
        
        ICS: InsightCacheService
        
        IM: InsightManager
        
        IE: InsightEngine
        
        DS: DataService
        """
        return self.services
    
    def getService(self,ID: str):
        """_summary_
        返回一个服务，以下是可用的key
        
        ICS: InsightCacheService
        
        IM: InsightManager
        
        IE: InsightEngine
        
        DS: DataService
        Args:
            ID (str): 这个服务的ID
        """
        return self.services[ID]
        
    