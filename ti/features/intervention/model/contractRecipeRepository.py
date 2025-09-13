

from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.intervention.model.model import INV_Contract_Recipe
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.symbol_service import SymbolService


class INV_CON_Recipe_Repository(IYamlRepository):
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService
    ):
        """
        负责获取contract recipe
        """
        self.yaml_parser = yaml_parser
        self.symbol = symbol_service
        # 在初始化时加载配方数据
        self._recipes_data = self._load_data()
    
    def get_all_recipe(self):
        recipies = []
        for contract_category_id in self._recipes_data:
            recipies.append(self.get_by_id(contract_category_id))
            
        return recipies
    
    def get_by_id(self,contract_category_id):
        """_summary_
        这个类负责把配方转换为数据模型
        Args:
            contract_category_id (_type_): _description_

        Returns:
            _type_: _description_  
        """
        contract_recipe = self._recipes_data[contract_category_id]
        duration = contract_recipe["duration"]
        view_recipe_id = contract_recipe["view_recipe_id"]
        
        contract_recipe = INV_Contract_Recipe(
            contract_category_id,
            duration,
            view_recipe_id
        )
    
        return contract_recipe
    
    def _load_data(self):
        """
        从YAML文件加载配方数据
        连同规则文件一起加载
        """
        try:
            # 检查规则文件是否为空
            rules_data = self.yaml.get_data(self.rule_file_path)
            
            if rules_data is None or rules_data == {}:
                # 规则文件为空，直接加载原始数据
                recipes_data = self.yaml.get_data(self.filePath)
                recipes_data = recipes_data.get('contract_recipes', {}) if recipes_data else {}
            else:
                # 规则文件不为空，使用parse_data方法解析
                recipes_data = self.yaml.parse_data(self.filePath, self.rule_file_path)
                recipes_data = recipes_data.get('contract_recipes', {})
            
            # 填充符号
            filled_recipes = self.symbol.fill_symbols(recipes_data)
            return filled_recipes
            
        except Exception as e:
            print(f"Error loading contract recipes data: {e}")
            return {}
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/intervention/model/data/contract_recipes.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/features/intervention/model/data/rules.yaml" #鉴于没有特殊规则，直接使用同样的空规则文件
    
    def save(self):
        return super().save()
    def load(self):
        return super().load()
    
    def delete(self, id):
        return super().delete(id)
    
    
# 数据现在从 YAML 文件加载