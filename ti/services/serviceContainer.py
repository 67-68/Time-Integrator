from ti.dataAccess.dataService import DataService
from ti.dataAccess.insightCacheService import InsightCacheService
from ti.dataAccess.insightManager import InsightManager
from ti.engine.insightEngine import InsightEngine
from ti.services.InterventionLoggerService import InterventionLogger
from ti.services.interventionService import InterventionService
from ti.services.realTimeMonitorService import RealTimeMonitor
from dataclasses import dataclass

@dataclass
class ServiceContainer:
    services = {}
        
    # 现在先不区分"哪一套的"IM, IE
    cache =  InsightCacheService()
    services["ICS"] = cache
    
    manager = InsightManager(cache)
    services["IM"] = manager
    
    engine = InsightEngine(cache)
    services["IE"] = engine
    
    dataService = DataService()
    services["DS"] = dataService
    
    monitor = RealTimeMonitor(dataService)
    services["RTM"] = monitor
    
    # Intervention功能相关
    intervention = InterventionService(monitor)
    services["IS"] = intervention
    

    
    logger = InterventionLogger()
    services["IL"] = logger
          
    def getServices(self):
        """_summary_
        返回一个字典，以下是可用的key
        
        ICS: InsightCacheService
        
        IM: InsightManager
        
        IE: InsightEngine
        
        DS: DataService
        
        IS: InterventionService
        
        IL: InterventionLogger
        
        RTM: RealTimeMonitor
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
        
    