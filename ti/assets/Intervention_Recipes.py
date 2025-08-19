from dataclasses import dataclass

@dataclass
class InterventionRecipe:
    intervention_id: str
    detector = None

meal_waste_intervention = InterventionRecipe("post_meal_waste")