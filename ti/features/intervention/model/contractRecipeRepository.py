

from ti.features.intervention.model.model import INV_Contract_Duration, INV_Contract_Recipe, INV_View_ID


class INV_CON_Recipe_Repository:
    def __init__(self):
        """
        负责获取contract recipe
        """
        self.recipe = INTERVENTION_CONTRACT_RECIPE
    
    def get_all_recipe(self):
        recipies = []
        for contract_category_id in self.recipe:
            recipies.append(self.get_recipe_by_id(contract_category_id))
            
        return recipies
    
    def get_recipe_by_id(self,contract_category_id):
        """_summary_
        这个类负责把配方转换为数据模型
        Args:
            contract_category_id (_type_): _description_

        Returns:
            _type_: _description_  
        """
        contract_recipe = INTERVENTION_CONTRACT_RECIPE[contract_category_id]
        duration = contract_recipe["duration"]
        view_recipe_id = contract_recipe["view_recipe_id"]
        
        contract_recipe = INV_Contract_Recipe(
            contract_category_id,
            duration,
            view_recipe_id
        )
    
        return contract_recipe
    
INTERVENTION_CONTRACT_RECIPE = {
    "post_eat_waste": {
        "duration": INV_Contract_Duration.TODAY.value,
        "view_recipe_id": INV_View_ID.POST_EAT_WASTE.value
    }
}