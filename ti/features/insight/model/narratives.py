from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.symbol_service import SymbolService


class InsightNarrator(IYamlRepository):
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService
    ):
        """
        辅助获取Insight Narrative数据
        """
        self.yaml_parser = yaml_parser
        self.symbol = symbol_service
        # 在初始化时加载叙事数据
        self._narratives_data = self._load_data()
    
    def get_universal_narrative(self, key: str):
        """
        获取通用叙事文本
        """
        universal = self._narratives_data.get('universal', {})
        return universal.get(key, [])
    
    def get_specific_narrative(self, action_type: str, narrative_key: str):
        """
        获取特定行动类型的叙事文本
        """
        specific = self._narratives_data.get('specific', {})
        action_data = specific.get(action_type, {})
        return action_data.get(narrative_key, None)
    
    def get_presentation(self, action_type: str, presentation_type: str):
        """
        获取展示文本
        """
        specific = self._narratives_data.get('specific', {})
        action_data = specific.get(action_type, {})
        presentation = action_data.get('presentation', {})
        return presentation.get(presentation_type, {})
    
    def _load_data(self):
        """
        从YAML文件加载叙事数据
        """
        try:
            # 直接加载原始数据
            narratives_data = self.yaml.get_data(self.filePath)
            narratives_data = narratives_data.get('insight_narratives', {}) if narratives_data else {}
            
            # 填充符号
            filled_narratives = self.symbol.fill_symbols(narratives_data)
            return filled_narratives
            
        except Exception as e:
            print(f"Error loading insight narratives data: {e}")
            return {}
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/insight/model/data/insight_narratives.yaml"
    
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
# 保留常量定义供外部使用
PEAK_TIMESPAN = "peak_timeSpan"
SHOW_RATIO = "show_ratio"
POST_EAT_WASTE = "post_eat_waste"