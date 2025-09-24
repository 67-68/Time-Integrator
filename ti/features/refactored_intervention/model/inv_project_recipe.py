from dataclasses import dataclass
from pydantic import BaseModel

from ti.features.refactored_intervention.model.inv_component_rule import INVComponentRule


class INVComponentRecipe(BaseModel):
    class_name: str
    rule: type[INVComponentRule]


class INVProjectRecipe(BaseModel):
    eventSources: dict[str,INVComponentRecipe] # source id: recipe
    views: list[INVComponentRecipe]
    project_id : str

@dataclass
class INVProjects:
    eventSources: dict[str,INVComponentRecipe] # source id: recipe
    views: list[INVComponentRecipe]
    project_id : str