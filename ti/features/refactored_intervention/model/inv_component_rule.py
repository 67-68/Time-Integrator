from pydantic import BaseModel

class INVComponentRule(BaseModel):
    pass

class EventSourceRule(INVComponentRule):
    pass

class ActionEventSourceRule(EventSourceRule):
    detector_id: str
    event_source_id: str
    # 不需要project id, 会传入
    
class INVViewRule(INVComponentRule):
    view_id: str