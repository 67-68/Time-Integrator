from dataclasses import dataclass
from ti.core.Interfaces.basic_event import BasicEvent


class InsightEvent(BasicEvent):
    pass

@dataclass
class SaveInsightCard(InsightEvent):
    event_id: str = "save_insight_card"
    card_uuid: str = None