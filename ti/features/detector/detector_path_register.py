from ti.model.plugin.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional


class DetectorPathRegister(ISymbolPathRegister):
    """
    Path register for detector feature functions and classes
    """
    
    def __init__(self):
        self._symbols: Dict[str, SymbolModel] = {}
        self.load_data()
        self._enum_mapping = {
            "post_eat_waste": "ti.features.detector.model.Detector_Recipe_ID.POST_EAT_WASTE.value",
            "unsettling_heart": "ti.features.detector.model.Detector_Recipe_ID.UNSETTLING_HEART.value",
            "post_bash_waste": "ti.features.detector.model.Detector_Recipe_ID.POST_BASH_WASTE.value"
        }
    
    @property
    def domain(self) -> str:
        return "detector"
    
    @property
    def enum_mapping(self) -> dict:
        return self._enum_mapping
    
    @property
    def class_file_path(self) -> str:
        return "ti/features/detector/model/data/detector_classes.yaml"
    
    @property
    def class_method_file_path(self) -> str:
        return "ti/features/detector/model/data/detector_class_methods.yaml"
    
    @property
    def function_file_path(self) -> str:
        return "ti/features/detector/model/data/detector_functions.yaml"
    
    @property
    def enum_file_path(self) -> str:
        return "ti/features/detector/model/data/detector_enums.yaml"
    
    def regist_symbol_path(self, symbol_model):
        return super().regist_symbol_path(symbol_model)
    
    def get_symbol_path(self, symbol_id):
        # First check if this is an enum value that needs special handling
        if symbol_id in self._enum_mapping:
            # Return a SymbolModel for the enum value
            return SymbolModel(
                symbol_type=SymbolType.ENUM_CLASS,
                symbol_path=self._enum_mapping[symbol_id],
                symbol_domain="detector"
            )
        
        # 使用基类的实现
        return super().get_symbol_path(symbol_id)
    
    def resolve_enum_symbol(self, symbol_ref: str) -> str:
        """
        解析枚举符号引用，返回完整的符号路径
        """
        if not symbol_ref.startswith("detector."):
            return symbol_ref
        
        enum_name = symbol_ref.split(".", 1)[1]
        
        # 硬编码枚举值映射
        enum_mapping = {
            "post_eat_waste": "ti.features.detector.model.Detector_Recipe_ID.POST_EAT_WASTE",
            "unsettling_heart": "ti.features.detector.model.Detector_Recipe_ID.UNSETTLING_HEART",
            "post_bash_waste": "ti.features.detector.model.Detector_Recipe_ID.POST_BASH_WASTE"
        }
        
        if enum_name in enum_mapping:
            return f"{enum_mapping[enum_name]}.value"
        
        return symbol_ref
    
    def search_symbol_data(self, symbol_type = None, domain = None):
        return super().search_symbol_data(symbol_type, domain)
    
    def get_symbol_model(self) -> Dict[str, SymbolModel]:
        """
        Get all symbol models
        """
        return self._symbols
    
    def load_data(self) -> None:
        """
        Load data from YAML files
        """
        # Load from separate files
        self._load_from_file(self.class_method_file_path, "class_methods")
        self._load_from_file(self.function_file_path, "functions")
        self._load_from_file(self.class_file_path, "classes")
        self._load_from_file(self.enum_file_path, "enum_classes")
    
    def _load_from_file(self, file_path, key):
        return super()._load_from_file(file_path, key)