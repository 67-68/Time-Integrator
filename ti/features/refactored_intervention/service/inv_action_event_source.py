from ti.core.eventBus import EventBus
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.refactored_intervention.model.intervention_trigger import InterventionTriggered
from ti.features.refactored_intervention.model.inv_component_rule import ActionEventSourceRule
from ti.features.refactored_intervention.model.special_events import INVSpecialEvent
from ti.features.refactored_intervention.service.IIntervention_Event_Source import IInterventionEventSource
from ti.services.realTimeMonitor import Monitor_Pack, RealTimeMonitor


class INVActionEventSource(IInterventionEventSource):
    """
    检测用户行为的EventSource

    Args:
        IInterventionEventSource (_type_): _description_
    """
    def __init__(
        self,
        repo: DetectorRepository,
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
        
        detector_recipe = self.rep.get_recipe_by_id(rule.detector_id)
        hook = detector_recipe.config.sequence.hook
        
        pack = Monitor_Pack(
            self.event_source_id,
            hook
        )
        
        self.monitor.add_monitor_to_thread(project_id,pack)
        
        self.bus.subscribe(f"{project_id}_{self.event_source_id}_pattern_detected",self.publish_event)
        

    def publish_event(self,content):
        triggered = InterventionTriggered(
            self.event_source_id,
            self.project_id,
            INVSpecialEvent.INTERVENE_USER.value # 目前仅支持这个，后续或许配置
        )
        
        self.bus.publish_event(InterventionTriggered,triggered)