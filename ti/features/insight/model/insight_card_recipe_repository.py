from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.symbol_service import SymbolService


class Insight_Card_Recipe_Repository(IYamlRepository):
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService
    ):
        """
        负责获取insight card recipe
        """
        self.yaml_parser = yaml_parser
        self.symbol = symbol_service
        # 在初始化时加载配方数据
        self._recipes_data = self._load_data()
    
    def get_fixed_recipes(self):
        """
        获取所有固定配方
        """
        return self._recipes_data.get('fixed_recipes', [])
    
    def get_conditional_recipes(self):
        """
        获取所有条件配方
        """
        return self._recipes_data.get('conditional_recipes', [])
    
    def _load_data(self):
        """
        从YAML文件加载配方数据
        """
        try:
            # 直接加载原始数据
            recipes_data = self.yaml.get_data(self.filePath)
            recipes_data = recipes_data.get('insight_card_recipes', {}) if recipes_data else {}
            
            # 填充符号
            filled_recipes = self.symbol.fill_symbols(recipes_data)
            return filled_recipes
            
        except Exception as e:
            print(f"Error loading insight card recipes data: {e}")
            return {}
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/insight/model/data/insight_card_recipes.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/features/insight/model/data/rules.yaml"
    
    def save(self):
        return super().save()
    def load(self):
        return super().load()
    
    def delete(self, id):
        return super().delete(id)

# 数据现在从 YAML 文件加载