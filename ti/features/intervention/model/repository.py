from ti.features.intervention.model.model import Intervention_ID, InterventionRecipe


class InterventionRepository:
    def __init__(self):
        pass
    
    def get_all_recipes(self):
        """_summary_
        这个函数会返回所有配方
        """
        recipe_dataClass = []
        
        for recipe_id in recipes:
            recipe_dataClass.append(self.get_recipe_by_id(recipe_id))
        
        return recipe_dataClass
    
    def get_recipe_by_id(self,intervention_id: str):
        """_summary_
        这个函数会返回id指向的配方

        Args:
            intervention_id (str): _description_
        """
        recipe = recipes[intervention_id]
        id = recipe["id"]
        state = recipe["state"]
        detector = recipe["detector"]
        
        recipe_dataClass = InterventionRecipe(id,state,detector = detector)
        
        return recipe_dataClass


recipes = {
    Intervention_ID.POST_EAT_WASTE.value: {
        "id":"post_meal_waste",
        "state":[
            "init"
        ]
    }
}