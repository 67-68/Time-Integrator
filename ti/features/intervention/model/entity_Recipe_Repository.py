from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.intervention.model.model import INV_Entity_Recipe
from ti.features.yaml_database.service.yaml_parser_service import YamlParser


class INV_Entity_Recipe_Repository(IYamlRepository):
    def __init__(
        self,
        yaml_parser: YamlParser
    ):
        """
        存储所有干涉实体的配方
        """
        self.yaml_parser = yaml_parser
        # 在初始化时加载配方数据
        self._recipes_data = self._load_data()
        
    def get_all_recipes(self):
        data = {}
        for recipe_id in self._recipes_data:
            data[recipe_id] = self.get_recipe_by_id(recipe_id)
        
        return data
    
    def get_recipe_by_id(self,recipe_id):
        recipe = self._recipes_data[recipe_id]
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
    
    def _load_data(self):
        """
        从YAML文件加载配方数据
        """
        try:
            # 直接加载原始数据
            recipes_data = self.yaml.get_data(self.filePath)
            recipes_data = recipes_data.get('entity_recipes', {}) if recipes_data else {}
            return recipes_data
            
        except Exception as e:
            print(f"Error loading entity recipes data: {e}")
            return {}
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/intervention/model/data/entity_recipes.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/features/intervention/model/data/rules.yaml"
    
    def save(self):
        return super().save()
    def load(self):
        return super().load()
    
    def delete(self, id):
        return super().delete(id)

# 数据现在从 YAML 文件加载
    