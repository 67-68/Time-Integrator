from ti.core.eventBus import EventBus
from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.refactored_intervention.model.inv_reducer import INVReducer
from ti.features.refactored_intervention.service.inv_project_factory import INVProjectFactory
from ti.services.realTimeMonitor import RealTimeMonitor


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
        monitor: RealTimeMonitor,
        detector_repository: DetectorRepository
    ):
        self.bus = bus
        self.reducer = INVReducer()
        self.projects = {}
        self.create_classes(monitor, detector_repository)
        
    def create_classes(self, monitor: RealTimeMonitor, detector_repository: DetectorRepository):
        """Create intervention projects using the factory"""
        factory = INVProjectFactory(self.bus, monitor, detector_repository)
        self.projects = factory.create_projects()
                
            
        