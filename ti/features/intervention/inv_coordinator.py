from ti.core.eventBus import EventBus
from ti.features.intervention.presenter.intervention_presenter import InterventionPresenter
from ti.features.intervention.view.intervention_view import InterventionView
from ti.model.yaml_repository import YamlRepository
from ti.features.intervention.service.inv_reducer import INVReducer
from ti.features.intervention.service.inv_project_factory import INVProjectFactory
from ti.model.yaml_repository import YamlRepository
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.symbol_service import SymbolService


class INVCoordinator:
    """
    The coordinator of Intervention Plugin
    have the responsibility to initialize
    contain
    - load recipe
    - create classes
    """
    def __init__(
        self,
        bus: EventBus,
        reducer: INVReducer,
        factory: INVProjectFactory
    ):
        self.bus = bus
        self.factory = factory
        self.reducer = reducer
        self.projects = {}
        self.presenter = None  # 初始化presenter属性
        self.create_classes()
        
    def create_classes(self):
        """Create intervention projects using the factory"""
        self.projects = self.factory.create_projects()
    
    def create_page(self) -> InterventionView:
        self.presenter = InterventionPresenter()  # 保存Presenter引用
        print("创建presenter")
        # View需要被显示，通常在调用此方法的地方调用view.show()
        return self.presenter.view
        
    