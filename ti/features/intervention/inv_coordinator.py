from ti.core.eventBus import EventBus
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
        self.create_classes()
        
    def create_classes(self):
        """Create intervention projects using the factory"""
        self.projects = self.factory.create_projects()
        print("=" *50)
        print("create projects")
        print("=" *50)
                
            
        