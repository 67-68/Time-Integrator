from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.symbol_service import SymbolService
from ti.features.intervention.model.model import INV_View_ID, INVEvent


class InterventionNarrator(IYamlRepository):
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService
    ):
        """_summary_
        辅助获取Narrative数据
        """
        self.yaml_parser = yaml_parser
        self.symbol = symbol_service
        # 在初始化时加载叙事数据
        self._narratives_data = self._load_data()
    
    def get_text_by_id(
        self,
        intervention_id: str,
        sementic_id: str
    ):
        """_summary_
        这个函数会返回id指向的Intervention类
        数据里面的sementic id 指向的数据

        Args:
            intervention_id (str): _description_
            sementic_id (str): _description_

        Returns:
            _type_: _description_
        """
        intervention_data = self._narratives_data.get(intervention_id, {})
        data = intervention_data.get(sementic_id, None)
        
        return data
    
    def _load_data(self):
        """
        从YAML文件加载叙事数据
        """
        try:
            # 直接加载原始数据
            narratives_data = self.yaml.get_data(self.filePath)
            narratives_data = narratives_data.get('intervention_narratives', {}) if narratives_data else {}
            
            # 填充符号
            filled_narratives = self.symbol.fill_symbols(narratives_data)
            return filled_narratives
            
        except Exception as e:
            print(f"Error loading intervention narratives data: {e}")
            return {}
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/intervention/model/data/intervention_narratives.yaml"
    
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