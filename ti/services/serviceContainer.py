from ti.UI.presenters.formatter import FormatService
from ti.core.eventBus import EventBus
from ti.dataAccess.dataService import DataService
from ti.dataAccess.insightCacheService import InsightCacheService
from ti.dataAccess.insightManager import InsightManager
from ti.engine.insightEngine import InsightEngine
from ti.features.intervention.InterventionLoggerService import InterventionLogger
from ti.features.intervention.interventionService import InterventionService
from ti.services.realTimeMonitorService import RealTimeMonitor
from dataclasses import dataclass


class ServiceContainer:
    def __init__(self):
        self.services = {}
            
        # 现在先不区分"哪一套的"IM, IE
        cache =  InsightCacheService()
        self.services["ICS"] = cache
        
        formatter = FormatService()
        self.services["FS"] = formatter
        
        manager = InsightManager(cache)
        self.services["IM"] = manager
        
        engine = InsightEngine(cache)
        self.services["IE"] = engine
        
        dataService = DataService()
        self.services["DS"] = dataService
        
        monitor = RealTimeMonitor(dataService)
        self.services["RTM"] = monitor
        
        # Intervention功能相关
        intervention = InterventionService(monitor,formatter)
        self.services["IS"] = intervention

        logger = InterventionLogger()
        self.services["IL"] = logger
        
        bus = EventBus()
        self.services["bus"] = bus
        
        
          
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
        
        FS: FormatService
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
        
    