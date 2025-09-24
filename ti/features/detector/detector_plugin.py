"""_summary_
Detector插件负责管理所有检测器的生命周期和协调
它继承ExtensionInterface和IPathRegisterProvider接口
"""

from ti.features.detector.detector_coordinator import DetectorCoordinator
from ti.model.plugin.function_contributions import FunctionContribution
from ti.model.plugin.function_provider_interface import IFunctionExtension
from ti.model.plugin.path_register_provider_interface import IPathRegisterProvider
from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.detector.detector_path_register import DetectorPathRegister
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.sessionCache import SessionCache
from ti.services.symbol_service import SymbolService


class DetectorPlugin(
    IFunctionExtension,
    IPathRegisterProvider
):
    def __init__(
        self,
        monitor: RealTimeMonitor,
        bus: EventBus,
        yaml_parser: YamlParser,
        cache: SessionCache
    ):
        """_summary_
        Detector插件的主类
        负责管理所有检测器的生命周期和协调
        """
        # 获取服务
        self.monitor = monitor
        self.bus = bus
        self.yaml_parser = yaml_parser
        self.cache = cache
        
        # 创建detector相关的服务
        self.repository = DetectorRepository(yaml_parser)
        self.factory = DetectorFactory(self.repository, cache)
        self.coordinator = DetectorCoordinator(self.repository, cache)

    # ------ 接口方法 ——----    
    
    @property
    def name(self):
        return "Detector"
    
    def initialize(self, eventBus: EventBus):
        """_summary_
        初始化detector插件
        在这里可以订阅相关事件
        Args:
            eventBus (_type_): _description_
        """
        self.bus = eventBus
        # 可以在这里订阅detector相关的事件
        # 例如：eventBus.subscribe("action_unit_recorded", self._on_action_recorded)
    
    def shutdown(self):
        """_summary_
        关闭detector插件
        清理资源
        """
        # 清理detector相关的资源
        pass
    
    # ------ 业务逻辑 ——----
    
    def get_factory(self) -> DetectorFactory:
        """_summary_
        获取detector工厂实例
        Returns:
            DetectorFactory: detector工厂
        """
        return self.factory
    
    def get_repository(self) -> DetectorRepository:
        """_summary_
        获取detector仓库实例
        Returns:
            DetectocRepository: detector仓库
        """
        return self.repository
    
    @staticmethod
    def register_class():
        return DetectorPathRegister
    
    @property
    def function_contributions(self):
        return [
            FunctionContribution(
                self.coordinator.get_detector,
                "get_detector"
            ),
            FunctionContribution(
                self.coordinator.get_factory,
                "get_detector_factory"
            ),
            FunctionContribution(
                self.coordinator.get_repository,
                "get_detector_repository"
            ),
        ]