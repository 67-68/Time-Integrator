from ti.features.intervention.model.model import Intervention_ID, InterventionEvent, InterventionRecipe, InterventionState


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
        recipe_states = recipe["state"]
        detector = recipe["detector"]
        initial_state = recipe["initial_state"]
        
        states_dataClass = {}
        
        for state_key in recipe_states:
            transitions = recipe_states[state_key]
            states_dataClass[state_key] = InterventionState(state_key,transitions)
        
        
        recipe_dataClass = InterventionRecipe(id,states_dataClass,initial_state,detector)
        
        return recipe_dataClass




recipes = {
    Intervention_ID.POST_EAT_WASTE.value: {
        "id":"post_eat_waste",
        "state":{
            "init": {
                InterventionEvent.USER_ACCEPTED:"create_intervention",
                InterventionEvent.USER_REJECTED:"ask_attribution"
            },
            "create_intervention":None
        },
        "initial_state":"init",
        "detector":None
        
    }
}
