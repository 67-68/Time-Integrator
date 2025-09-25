from dataclasses import dataclass
from pydantic import BaseModel
from ti.features.intervention.model.stored.inv_component_rule import ActionEventSourceRule, INVComponentRule
from ti.features.intervention.model.stored.inv_view_state import INVViewRecipe

class INVComponentRecipe(BaseModel):
    class_name: str
    rule: type[INVComponentRule]


class INVProjectRecipe(BaseModel):
    event_sources: dict[str,INVComponentRecipe] # source id: recipe
    views: list[INVComponentRecipe]
    project_id : str

@dataclass
class INVProjects:
    eventSources: dict[str,ActionEventSourceRule] # source id: recipe
    views: dict[INVViewRecipe]
    project_id : str