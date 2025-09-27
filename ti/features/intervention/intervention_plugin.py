from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.intervention.inv_coordinator import INVCoordinator
from ti.features.intervention.model.stored.inv_project_model import INVProjectModel
from ti.features.intervention.model.stored.inv_project_recipe import INVProjectRecipe
from ti.features.intervention.service.inv_project_factory import INVProjectFactory
from ti.features.intervention.service.inv_reducer import INVReducer
from ti.model.yaml_repository import YamlRepository
from ti.services.function_service import FunctionService
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.symbol_service import SymbolService


class InterventionPlugin(
    ExtensionInterface
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
        # 使用function service获取detector repository
        detec_repo = function.get_function("get_detector_repository")()
        project_repository = YamlRepository("ti/features/intervention/model/inv_projects.yaml",INVProjectModel, identifier_field="project_id")
        project_recipe_repository = YamlRepository("ti/features/intervention/model/data/inv_recipe.yaml",INVProjectRecipe, identifier_field="project_id")
        
        factory = INVProjectFactory(
            bus,
            monitor,
            detec_repo,
            symbol_service,
            project_recipe_repository
        )
        
        reducer = INVReducer(
            project_repository,
            bus
        )
        
        self.coordinator = INVCoordinator(
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
    
