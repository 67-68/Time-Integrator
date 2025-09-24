
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister

from ti.services.function_service import FunctionService
from ti.services.page_factory import PageFactory
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.insight.model.narratives import InsightNarrator
from ti.features.intervention.service.logger import InterventionLogger
from ti.features.translation.service.translator_service import Translator
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.loggerService import LoggerService
from ti.services.dataService import DataService
from ti.features.insight.service.insightCacheService import InsightCacheService
from ti.features.insight.service.insightManager import InsightManager
from ti.features.insight.service.insightEngine import InsightEngine
from ti.features.insight.service.formatter import InsightFormatService
from ti.services.realTimeMonitor import RealTimeMonitor
from dataclasses import dataclass

from ti.services.sessionCache import SessionCache
from ti.services.symbol_service import SymbolService


class ServiceContainer:
    def __init__(self):
        self.services = {} # 用来一般查找，存储简称
        self._services = {} #用来自动查找，存储全称
            
        func_service = FunctionService()
        self.services["function"] = func_service
        self._services[FunctionService] = func_service
            
        session = SessionCache()
        self.services["session"] = session
        self._services[SessionCache] = session
            
        translator = Translator()
        self.services["translator"] = translator
        self._services[Translator] = translator
        
        yaml_parser = YamlParser()
        self.services["yaml_parser"] = yaml_parser
        self._services[YamlParser] = yaml_parser
            
        cache =  InsightCacheService(yaml_parser)
        self.services["ICS"] = cache
        self._services[InsightCacheService] = cache
        
        symbol = SymbolService()
        self.services["symbol"] = symbol
        self._services[SymbolService] = symbol
        
        narrator = InsightNarrator(yaml_parser,symbol)
        
        formatter = InsightFormatService(narrator)
        self.services["FS"] = formatter
        self._services[InsightFormatService] = formatter
        
        dataService = DataService()
        self.services["DS"] = dataService
        self._services[DataService] = dataService
        
        bus = EventBus()
        self.services["bus"] = bus
        self._services[EventBus] = bus
        
        page_fac = PageFactory(bus)
        self.services["page_factory"] = page_fac
        self._services[PageFactory] = page_fac
        
        monitor = RealTimeMonitor(dataService, bus)
        self.services["RTM"] = monitor
        self._services[RealTimeMonitor] = monitor
    
        register = ExtensionRegister(bus)
        self.services["ER"] = register
        self._services[ExtensionRegister] = register

        loader = DynamicExtensionLoader(register,self,bus,symbol,func_service)
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
    
    def create_logger_service(self, feature_base_dir: str, feature_name: str):
        """
        创建LoggerService实例
        
        Args:
            feature_base_dir: 功能模块的基础目录路径
            feature_name: 功能模块名称
            
        Returns:
            LoggerService实例
        """
        return LoggerService(feature_base_dir, feature_name)
    
    