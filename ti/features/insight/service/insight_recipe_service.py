from typing import Dict, Any
from ti.features.insight.service.insight_interfaces import IInsightRecipeService
from ti.services.loggerService import LoggerService


class InsightRecipeService(IInsightRecipeService):
    """洞察配方服务实现"""
    
    def __init__(self):
        self.logger = LoggerService("./ti/features/insight", "recipe_service")
    
    def load_recipes(self) -> Dict[str, Any]:
        """加载洞察卡片配方"""
        self.logger.log("配方加载", "开始加载洞察卡片配方")
        
        from ti.model.yaml_repository import YamlRepository
        from ti.features.insight.model.insight_card_recipe_models import FixedRecipe, ConditionalRecipe
        
        # 使用YamlRepository加载配方数据
        recipe_repo = YamlRepository(
            "ti/features/insight/model/data/insight_card_recipes.yaml", 
            dict,
            identifier_field="insight_card_recipes"
        )
        
        # 获取配方数据
        recipes_data = recipe_repo.get_by_id("insight_card_recipes")
        
        fixed_recipes = []
        conditional_recipes = []
        
        if recipes_data and "insight_card_recipes" in recipes_data:
            recipes_container = recipes_data["insight_card_recipes"]
            
            # 解析固定配方
            if "fixed_recipes" in recipes_container:
                for recipe_data in recipes_container["fixed_recipes"]:
                    fixed_recipes.append(FixedRecipe(**recipe_data))
            
            # 解析条件配方
            if "conditional_recipes" in recipes_container:
                for recipe_data in recipes_container["conditional_recipes"]:
                    conditional_recipes.append(ConditionalRecipe(**recipe_data))
        
        self.logger.log("配方加载", f"加载了 {len(conditional_recipes)} 个条件配方和 {len(fixed_recipes)} 个固定配方")
        
        return {
            "fixed_recipes": fixed_recipes,
            "conditional_recipes": conditional_recipes
        }