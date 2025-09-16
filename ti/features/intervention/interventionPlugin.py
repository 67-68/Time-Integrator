"""_summary_
鉴于这个功能覆盖面很广
不仅仅是一个页面内的交互而是牵扯到不同的页面和生命周期
因此选择Coodinator(MVP/MVC以上的层级)来协调而非Controller(MVC)
"""

from ti.core.Interfaces.path_register_provider_interface import IPathRegisterProvider
from ti.features.insight.view.insight_card import InsightCard
from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.detector.detectorRepository import DetectocRepository
from ti.features.intervention.cardOrchestrator import INV_Card_Orchestrator
from ti.features.intervention.coordinator import InterventionCoordinator
from ti.features.intervention.intervention_contract_orchestrator import INV_Contract_Orchestrator
from ti.features.intervention.intervention_path_register import INV_PathRegister
from ti.features.intervention.model.contractRecipeRepository import INV_CON_Recipe_Repository
from ti.features.intervention.model.contractRepository import INV_ContractRepository
from ti.features.intervention.model.entity_Recipe_Repository import INV_Entity_Recipe_Repository
from ti.features.intervention.service.cardFactory import INV_Card_Factory, InterventionFactory_Pack
from ti.features.intervention.service.contractService import INV_ContractService
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.service.logger import InterventionLogger
from ti.features.intervention.model.narratives import InterventionNarrator
from ti.features.intervention.model.view_repository import INV_Card_Repository
from ti.features.intervention.presenter.cardPresenter import InterventionPresenter
from ti.features.intervention.service.mapping import InterventionMapping
from ti.features.intervention.service.register import INV_ContractRegister
from ti.features.intervention.service.stateMachine import INV_StateService
from ti.features.intervention.serviceContainer import INV_ServiceContainer
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.sessionCache import SessionCache
from ti.services.symbol_service import SymbolService


class InterventionPlugin(
    ExtensionInterface,
    IPathRegisterProvider
):
    def __init__(
        self,
        monitor: RealTimeMonitor,
        bus: EventBus,
        detector_rep: DetectocRepository,
        symbol_service: SymbolService,
        yaml_parser: YamlParser,
    ):
        """_summary_
        这是Intervention插件的主类
        掌管不同生命周期下的Intervention应该做什么
        首先它会获取卡片，然后在后面卡片制造的时候把它塞进去
        插件应该是先于主体部分加载的
        """
        # 获取服务
        self.monitor = monitor
        self.bus = bus
        self.yaml_parser = yaml_parser
        
        # 首先加载基础设施
        # path_register = INV_PathRegister()
        # self.path_register = path_register 在extension中创建
        
        # 创建服务
        self.container = INV_ServiceContainer()
        self.container.add_service("bus",bus)
        self.container.add_service("monitor",monitor)
        
        narrator = InterventionNarrator(yaml_parser, symbol_service)
        self.container.add_service("narrator",narrator)
        
        formatter = INV_Formatter(narrator)
        self.container.add_service("formatter",formatter)
        
        view_repository = INV_Card_Repository(
            formatter,
            symbol_service,
            yaml_parser
        )
        
        self.container.add_service("view_repository",view_repository)
        
        view_factory = INV_Card_Factory(formatter)
        self.container.add_service("view_factory",view_factory)
        
        logger = InterventionLogger()
        self.container.add_service("logger",logger)
        
        entity_rep = INV_Entity_Recipe_Repository(yaml_parser)
        self.container.add_service("entity_rep",entity_rep)
        
        mapping = InterventionMapping(entity_rep)
        self.container.add_service("mapping",mapping)
        
        register = INV_ContractRegister(monitor,detector_rep)
        self.container.add_service("register",register)
        
        # Register intervention path register with symbol service
        intervention_register = INV_PathRegister()
        symbol_service.regist_register(intervention_register)
        
        contract_recipe_repos = INV_CON_Recipe_Repository(yaml_parser,symbol_service)
        self.container.add_service("CON_recipe_repos",contract_recipe_repos)
        
        contract_repository = INV_ContractRepository()
        self.container.add_service("contract_repository",contract_repository)
        
        contract_service = INV_ContractService(contract_repository,contract_recipe_repos,register,logger)
        self.container.add_service("contract_service",contract_service)
        
        stateService = INV_StateService()
        self.container.add_service("stateService",stateService)
        
        card_orchestrator = INV_Card_Orchestrator(
            view_factory,
            formatter,
            view_repository,
            self.container
        )
        
        contract_orchestrator = INV_Contract_Orchestrator(
            contract_recipe_repos,
            contract_service,
            contract_repository,
            bus,
        )
    
        self.coordinator = InterventionCoordinator(
            self.container,
            card_orchestrator,
            contract_orchestrator,
            bus
        )
        
        
    
    # ------ 接口方法 ——----    
    
    @property
    def name(self):
        return "Intervention"
    
    def initialize(self, eventBus:EventBus):
        """_summary_
        目前暂定接受UI卡片完成的信号
        直接塞进UI
        在未来可能会考虑设计UI积木语法
        Args:
            eventBus (_type_): _description_
        """
        eventBus.subscribe("insight_card_ui_created",self._on_card_created)
        self.bus = eventBus
    
    def shutdown(self):
        return super().shutdown()
    
    # ------ 业务逻辑 ——----
    def _on_card_created(self,data: tuple):
        self.coordinator.process_insight_card(data)
    
                
    @staticmethod
    def register_class():
        return INV_PathRegister