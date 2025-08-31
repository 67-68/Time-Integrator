from ti.UI.presenters.formatter import FormatService
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister
from ti.dataAccess.dataService import DataService
from ti.dataAccess.insightCacheService import InsightCacheService
from ti.dataAccess.insightManager import InsightManager
from ti.domain.detector.detectorFactory import DetectorFactory
from ti.domain.detector.detectorRepository import DetectocRepository
from ti.engine.insightEngine import InsightEngine
from ti.features.intervention.service.logger import InterventionLogger
from ti.services.realTimeMonitor import RealTimeMonitor
from dataclasses import dataclass


class ServiceContainer:
    def __init__(self):
        self.services = {} # 用来一般查找，存储简称
        self._services = {} #用来自动查找，存储全称
            
        cache =  InsightCacheService()
        self.services["ICS"] = cache
        self._services[InsightCacheService] = cache
        
        detector_rep = DetectocRepository()
        self.services["DR"] = detector_rep
        self._services[DetectocRepository] = detector_rep
        
        detector_fac = DetectorFactory(detector_rep,cache)
        self.services["DF"] = detector_fac
        self._services[DetectorFactory] = detector_fac
        
        formatter = FormatService()
        self.services["FS"] = formatter
        self._services[FormatService] = formatter
        
        manager = InsightManager(cache)
        self.services["IM"] = manager
        self._services[InsightManager] = manager
        
        engine = InsightEngine(cache,detector_fac)
        self.services["IE"] = engine
        self._services[InsightEngine] = engine
        
        dataService = DataService()
        self.services["DS"] = dataService
        self._services[DataService] = dataService
        
        bus = EventBus()
        self.services["bus"] = bus
        self._services[EventBus] = bus
        
        monitor = RealTimeMonitor(dataService,detector_fac,bus)
        self.services["RTM"] = monitor
        self._services[RealTimeMonitor] = monitor
    
        register = ExtensionRegister(bus)
        self.services["ER"] = register
        self._services[ExtensionRegister] = register
        
        loader = DynamicExtensionLoader(register,self)
        self.services["loader"] = loader
        self._services[DynamicExtensionLoader] = loader
        
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
        
        bus
        
        DR
        
        DF
        
        ER
        """
        
        return self.services
    
    def getService(self,ID: str):
        """_summary_
        返回一个服务，以下是可用的key
        """
        return self.services[ID]
    
    def register_service(self, service_instance, service_type=None):
        # 我们可以按类型来注册服务
        service_key = service_type or type(service_instance)
        self._services[service_key] = service_instance
    
    def get_class_service(self,ID):
        """_summary_
        返回一个服务，以下是可用的key
        """
        return self._services[ID]
    
    