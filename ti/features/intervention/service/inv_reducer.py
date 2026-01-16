


from ti.core.eventBus import EventBus
from ti.features.intervention.model.stored.inv_project_model import INVProjectModelUpdated
from ti.features.intervention.model.events.intervention_trigger import InterventionTriggered
from ti.features.intervention.model.events.special_events import AddToInsightCardEvent, InterveneUserEvent
from ti.model.yaml_repository import YamlRepository


class INVReducer():
    def __init__(
        self,
        project_rep:YamlRepository,
        bus: EventBus
    ):
        """
        监听所有project的事件
        处理完成之后发出去
        """
        self.rep = project_rep
        self.bus = bus
    
    def reduce(self,trigger: InterventionTriggered):
        project_id = trigger.inv_project_id
        special_events = trigger.special_events
        
        # 找到project
        project_model = self.rep.get_by_id(project_id)
        
        for special_event in special_events:
            match special_event:
                case InterveneUserEvent():
                    project_model.condition_met = True
                case AddToInsightCardEvent():
                    self.bus.publish_event(AddToInsightCardEvent,special_event)
        
        self.rep.add_model(project_model)
        event = INVProjectModelUpdated(project_model)
        self.bus.publish_event(INVProjectModelUpdated,event)
        
    