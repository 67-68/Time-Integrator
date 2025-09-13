from dataclasses import dataclass
from typing import Dict, List

from ti.core.Interfaces.model.repository_interface import IRepository
from ti.features.insight.interface.generator_interface import ICardGenerator
from ti.features.insight.model.insight_card_repository import InsightCardRepository


class InsightRecipeProvider:
    def __init__(
        self,
        card_rep: InsightCardRepository
    ):
        """
        这个类管理配方的获取
        它登记不同的register
        他们的generator和narrative
        """
        self.card_rep = card_rep
        self.recipe_registrations: Dict[str, InsightRecipeRegistration] = {}
    
    def register_recipes(self, registration: 'InsightRecipeRegistration') -> None:
        """
        Register an InsightRecipeRegistration
        """
        # 使用生成器类名作为注册键
        name = registration.recipe_name
        self.recipe_registrations[name] = registration
        print(f"Registered recipe generator: {name}")

    def get_today_recipe(self) -> List[dict]:
        """
        返回所有duration = TODAY的配方
        如果card_rep中已存在相同类型的卡片，则不包含该配方
        """
        today_recipes = []
        
        for registration in self.recipe_registrations.values():
            for recipe in registration.recipes:
                # 检查是否为今天的配方
                if recipe.get('duration') == "core.Duration.TODAY.value":
                    # 检查是否已存在相同类型的卡片
                    card_type_id = recipe.get('id') or recipe.get('detector', '')
                    existing_cards = self.card_rep.get_by_card_type(card_type_id)
                    
                    # 如果不存在相同类型的卡片，则包含该配方
                    if not existing_cards:
                        today_recipes.append(recipe)
                    else:
                        print(f"Skipping recipe {card_type_id} - already exists in card repository")
        
        return today_recipes

    def get_all_recipes(self) -> List[dict]:
        """
        返回所有已注册的配方
        """
        all_recipes = []
        for registration in self.recipe_registrations.values():
            all_recipes.extend(registration.recipes)
        return all_recipes

    def get_recipes_by_generator(self, generator_name: str) -> List[dict]:
        """
        按生成器名称获取配方
        """
        registration = self.recipe_registrations.get(generator_name)
        return registration.recipes if registration else []


@dataclass
class InsightRecipeRegistration:
    recipe_name: str
    recipes: list
    generator: type[ICardGenerator]
    narrative_repotory: type[IRepository]