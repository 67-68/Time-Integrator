from ti.core.eventBus import EventBus
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.model.yaml_repository import YamlRepository
from ti.features.intervention.model.events.intervention_trigger import InterventionTriggered
from ti.features.intervention.model.events.special_events import INVSpecialEvent
from ti.features.intervention.model.stored.inv_component_rule import ActionEventSourceRule
from ti.features.intervention.service.IIntervention_Event_Source import IInterventionEventSource
from ti.services.realTimeMonitor import Monitor_Pack, RealTimeMonitor


class INVActionEventSource(IInterventionEventSource):
    """
    检测用户行为的EventSource

    Args:
        IInterventionEventSource (_type_): _description_
    """
    def __init__(
        self,
        repo: YamlRepository,
        monitor: RealTimeMonitor
    ):
        self.rep = repo
        self.monitor = monitor
    
    def initialize(
        self,
        project_id: str,
        bus: EventBus,
        rule: ActionEventSourceRule
    ):
        self.project_id = project_id
        self.bus = bus
        self.event_source_id = rule.event_source_id
        
        # 先检查仓库中所有可用的配方
        all_recipes = self.rep.get_all()
        print(f"[DEBUG] Available recipes in repository: {list(all_recipes.keys()) if hasattr(all_recipes, 'keys') else 'N/A'}")
        
        detector_recipe = self.rep.get_by_id(rule.detector_id)
        print(f"[DEBUG] Looking for detector recipe with ID: {rule.detector_id}")
        print(f"[DEBUG] Found recipe: {detector_recipe}")
        if detector_recipe is None:
            raise ValueError(f"Detector recipe '{rule.detector_id}' not found in repository")
        hook = detector_recipe.config.sequence.hook
        
        pack = Monitor_Pack(
            rule.detector_id,  # detector recipe ID
            self.event_source_id,  # monitor identifier
            hook
        )
        
        # 检查线程是否存在，如果不存在则创建
        if project_id not in self.monitor.list_threads():
            # 使用现有的DetectorRepository创建DetectorFactory
            from ti.features.detector.model.detectorFactory import DetectorFactory
            from ti.services.symbol_service import SymbolService
            symbol_service = SymbolService()
            detector_factory = DetectorFactory(self.rep, symbol_service)
            self.monitor.create_thread(project_id, detector_factory)
        
        self.monitor.add_monitor_to_thread(project_id, pack)
        
        self.bus.subscribe(f"{project_id}_{self.event_source_id}_pattern_detected",self.publish_event)
        

    def publish_event(self,content):
        triggered = InterventionTriggered(
            self.event_source_id,
            self.project_id,
            INVSpecialEvent.INTERVENE_USER.value # 目前仅支持这个，后续或许配置
        )
        
        self.bus.publish_event(InterventionTriggered,triggered)