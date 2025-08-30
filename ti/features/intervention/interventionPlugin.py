"""_summary_
鉴于这个功能覆盖面很广
不仅仅是一个页面内的交互而是牵扯到不同的页面和生命周期
因此选择Coodinator(MVP/MVC以上的层级)来协调而非Controller(MVC)
"""

from ti.UI.views.analysis.trendCard import InsightCard
from ti.core.Interfaces.Extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.intervention.coordinator import InterventionCoordinator
from ti.features.intervention.model.entity_Recipe_Repository import INV_Entity_Recipe_Repository
from ti.features.intervention.service.cardFactory import InterventionCard_Factory, InterventionFactory_Pack
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.service.logger import InterventionLogger
from ti.features.intervention.model.narratives import InterventionNarrator
from ti.features.intervention.model.repository import INV_Card_Repository
from ti.features.intervention.presenter.cardPresenter import InterventionPresenter
from ti.features.intervention.service.mapping import InterventionMapping
from ti.features.intervention.serviceContainer import INV_ServiceContainer
from ti.services.realTimeMonitorService import RealTimeMonitor
from ti.services.sessionCache import SessionCache


class InterventionPlugin(ExtensionInterface):
    def __init__(
        self,
        monitor: RealTimeMonitor,
        bus: EventBus
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
        
        # 创建服务
        self.container = INV_ServiceContainer()
        
        narrator = InterventionNarrator()
        self.container.add_service("narrator",narrator)
        
        formatter = INV_Formatter(narrator)
        self.container.add_service("formatter",formatter)
        
        view_repository = INV_Card_Repository(formatter)
        self.container.add_service("view_repository",view_repository)
        
        view_factory = InterventionCard_Factory(view_repository)
        self.container.add_service("view_factory",view_factory)
        
        logger = InterventionLogger()
        self.container.add_service("logger",logger)
        
        entity_rep = INV_Entity_Recipe_Repository()
        self.container.add_service("entity_rep",entity_rep)
        
        mapping = InterventionMapping(entity_rep)
        self.container.add_service("mapping",mapping)
        
        self.coordinator = InterventionCoordinator(self.container)
        
        
    
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
        self.coordinator.process_insight_card()
                
        