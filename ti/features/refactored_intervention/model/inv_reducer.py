


from ti.core.eventBus import EventBus
from ti.features.refactored_intervention.model.intervention_project import INVProjectModelUpdated
from ti.features.refactored_intervention.model.intervention_trigger import InterventionTriggered
from ti.features.refactored_intervention.model.inv_project_repository import INVProjectRepository
from ti.features.refactored_intervention.model.special_events import INVSpecialEvent


class INVReducer():
    def __init__(
        self,
        project_rep:INVProjectRepository,
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
                case INVSpecialEvent.INTERVENE_USER.value:
                    project_model.condition_met = True
        
        self.rep.add_model(project_model)
        event = INVProjectModelUpdated(project_model)
        self.bus.publish_event(INVProjectModelUpdated,event)
        
    