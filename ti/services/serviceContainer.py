
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister

from ti.model.strategy.strategy_repository import StrategyRepository
from ti.services.function_service import FunctionService
from ti.services.page_factory import PageFactory
from ti.features.translation.service.translator_service import Translator
from ti.services.loggerService import LoggerService
from ti.services.dataService import DataService
from ti.features.insight.service.formatter import InsightFormatService
from ti.services.realTimeMonitor import RealTimeMonitor
from dataclasses import dataclass

from ti.services.sessionCache import SessionCache
from ti.services.symbol_service import SymbolService


class ServiceContainer:
    def __init__(self):
        self.services = {} # 用来一般查找，存储简称
        self._services = {} #用来自动查找，存储全称
            
        strategy_rep = StrategyRepository.get_instance()
        self.services["strategy"] = strategy_rep
        self._services[StrategyRepository] = strategy_rep
            
        func_service = FunctionService()
        self.services["function"] = func_service
        self._services[FunctionService] = func_service
            
        session = SessionCache()
        self.services["session"] = session
        self._services[SessionCache] = session
            
        translator = Translator()
        self.services["translator"] = translator
        self._services[Translator] = translator
        
        
        symbol = SymbolService()
        self.services["symbol"] = symbol
        self._services[SymbolService] = symbol
        
        formatter = InsightFormatService()
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

        loader = DynamicExtensionLoader(register,self,bus,symbol,func_service,strategy_rep)
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
    
    