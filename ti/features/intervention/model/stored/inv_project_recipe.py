from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Any
from ti.features.intervention.model.stored.inv_component_rule import ActionEventSourceRule, INVComponentRule
from ti.features.intervention.model.stored.inv_view_state import INVViewRecipe

class INVComponentRecipe(BaseModel):
    class_name: str
    rule: Dict[str, Any]  # 包含类型信息和规则数据


class INVProjectRecipe(BaseModel):
    event_sources: dict[str,INVComponentRecipe] # source id: recipe
    views: dict[str,INVComponentRecipe] # view id: recipe
    project_id : str

@dataclass
class INVProjects:
    eventSources: dict[str,ActionEventSourceRule] # source id: recipe
    views: dict[str,INVViewRecipe] # view id: view instance
    project_id : str