from ti.features.intervention.model.model import INV_Entity_Recipe


class INV_Entity_Recipe_Repository:
    def __init__(self):
        """
        存储所有干涉实体的配方
        """
        self.entity_recipies = ENTITY_RECIPE
        
    def get_all_recipes(self):
        data = {}
        for recipe_id in self.entity_recipies:
            data[recipe_id] = self.get_recipe_by_id(recipe_id)
        
        return data
    
    def get_recipe_by_id(self,recipe_id):
        recipe = self.entity_recipies[recipe_id]
        view_id = recipe["card_id"]
        contract_recipe_id = recipe["contract_id"]
        insight_card_id = recipe["insight_card_id"]
        
        entity_recipe = INV_Entity_Recipe(
            insight_card_id,
            recipe_id,
            contract_recipe_id,
            view_id
        )
        
        return entity_recipe
        

ENTITY_RECIPE = {
    "post_eat_waste": {
        "card_id": "post_eat_waste",
        "contract_id":"post_eat_waste",
        "insight_card_id":"post_eat_waste"
    }
}
    