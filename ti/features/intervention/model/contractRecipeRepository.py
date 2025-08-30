

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
        
        return self.recipe[contract_category_id]

INTERVENTION_CONTRACT_RECIPE = {
    
}