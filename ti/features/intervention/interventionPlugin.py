from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.intervention.intervention_path_register import INV_PathRegister
from ti.features.intervention.inv_coordinator import INVCoordinator
from ti.features.intervention.service.inv_project_factory import INVProjectFactory
from ti.features.intervention.service.inv_reducer import INVReducer
from ti.model.plugin.path_register_provider_interface import IPathRegisterProvider
from ti.model.yaml_repository import YamlRepository
from ti.services.function_service import FunctionService
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.symbol_service import SymbolService


class InterventionPlugin(
    ExtensionInterface,
    IPathRegisterProvider
):
    def __init__(
        self,
        bus:EventBus,
        monitor: RealTimeMonitor,
        function: FunctionService,
        symbol_service: SymbolService
    ):
        """_summary_
        这是Intervention插件的主类
        创建Coordinator之后完成
        插件应该是先于主体部分加载的
        """
        detec_fac = function.get_function("get_detector_factory")
        project_repository = YamlRepository("ti/features/refactored_intervention/model/inv_projects.yaml")
        project_recipe_repository = YamlRepository("ti/features/refactored_intervention/model/inv_project_recipe.yaml")
        
        factory = INVProjectFactory(
            bus,
            monitor,
            detec_fac,
            symbol_service,
            project_recipe_repository
        )
        
        reducer = INVReducer(
            project_repository,
            bus
        )
        
        coordinator = INVCoordinator(
            bus,
            reducer,
            factory
        )
        
    # ------ 接口方法 ——----    
    
    @property
    def name(self):
        return "Intervention"
    
    def initialize(self, eventBus:EventBus):
        pass
    
    def shutdown(self):
        return super().shutdown()
    
    @staticmethod
    def register_class():
        return INV_PathRegister