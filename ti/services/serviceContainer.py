
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister

from ti.features.core_view.service.page_factory import PageFactory
from ti.services.synthesizer_service import Synthesizer
from ti.features.detector.detectorFactory import DetectorFactory
from ti.features.detector.detectorRepository import DetectocRepository
from ti.features.insight.model.narratives import InsightNarrator
from ti.features.intervention.service.logger import InterventionLogger
from ti.features.translation.service.translator_service import Translator
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.dataAccess.dataService import DataService
from ti.services.dataAccess.insightCacheService import InsightCacheService
from ti.services.dataAccess.insightManager import InsightManager
from ti.services.engine.insightEngine import InsightEngine
from ti.services.formatter import FormatService
from ti.services.realTimeMonitor import RealTimeMonitor
from dataclasses import dataclass

from ti.services.symbol_service import SymbolService


class ServiceContainer:
    def __init__(self):
        self.services = {} # 用来一般查找，存储简称
        self._services = {} #用来自动查找，存储全称
            
        translator = Translator()
        self.services["translator"] = translator
        self._services[Translator] = translator
            
        cache =  InsightCacheService()
        self.services["ICS"] = cache
        self._services[InsightCacheService] = cache
        
        syn = Synthesizer()
        self.services["syn"] = syn
        self._services[Synthesizer] = syn
        
        yaml_parser = YamlParser()
        self.services["yaml_parser"] = yaml_parser
        self._services[YamlParser] = yaml_parser
        
        symbol = SymbolService()
        self.services["symbol"] = symbol
        self._services[SymbolService] = symbol
        
        detector_rep = DetectocRepository()
        self.services["DR"] = detector_rep
        self._services[DetectocRepository] = detector_rep
        
        detector_fac = DetectorFactory(detector_rep,cache)
        self.services["DF"] = detector_fac
        self._services[DetectorFactory] = detector_fac
        
        narrator = InsightNarrator(yaml_parser,symbol)
        
        formatter = FormatService(narrator)
        self.services["FS"] = formatter
        self._services[FormatService] = formatter
        
        dataService = DataService()
        self.services["DS"] = dataService
        self._services[DataService] = dataService
        
        bus = EventBus()
        self.services["bus"] = bus
        self._services[EventBus] = bus
        
        page_fac = PageFactory(bus)
        self.services["page_factory"] = page_fac
        self._services[PageFactory] = page_fac
        
        monitor = RealTimeMonitor(dataService,detector_fac,bus)
        self.services["RTM"] = monitor
        self._services[RealTimeMonitor] = monitor
    
        register = ExtensionRegister(bus)
        self.services["ER"] = register
        self._services[ExtensionRegister] = register

        loader = DynamicExtensionLoader(register,self,bus,symbol)
        self.services["loader"] = loader
        self._services[DynamicExtensionLoader] = loader
    
    
        
        
        
        
    def getServices(self):
        """_summary_
        返回一个字典
        """
        
        return self.services
    
    def getService(self,ID: str):
        """_summary_
        返回一个服务
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
    
    