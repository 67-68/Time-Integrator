from enum import Enum
from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional


class INV_PathRegister(ISymbolPathRegister):
    """
    Path register for intervention feature functions and classes
    """
    
    def __init__(self):
        self._symbols: Dict[str, SymbolModel] = {}
        self.load_data()
        self._enum_mapping = {
            "USER_ACCEPTED": "ti.features.intervention.model.model.INVEvent.USER_ACCEPTED.value",
            "USER_REJECTED": "ti.features.intervention.model.model.INVEvent.USER_REJECTED.value", 
            "INTERVENTION_CREATED": "ti.features.intervention.model.model.INVEvent.INTERVENTION_CREATED.value",
            "END_INTERVENTION": "ti.features.intervention.model.model.INV_Special_States.END_INTERVENTION.value",
            "ACCEPTED_CONTRACT": "ti.features.intervention.model.model.INV_Special_States.ACCEPTED_CONTRACT.value"
        }
    
    @property
    def enum_mapping(self):
        return self._enum_mapping
    @property
    def domain(self) -> str:
        return "intervention"
    
    @property
    def class_file_path(self) -> str:
        return "ti/features/intervention/model/data/intervention_classes.yaml"
    
    @property
    def class_method_file_path(self) -> str:
        return "ti/features/intervention/model/data/intervention_class_methods.yaml"
    
    @property
    def function_file_path(self) -> str:
        return "ti/features/intervention/model/data/intervention_functions.yaml"
    
    @property
    def enum_file_path(self) -> str:
        return "ti/features/intervention/model/data/intervention_enums.yaml"
    
    def get_symbol_path(self, symbol_id):
        return super().get_symbol_path(symbol_id)
    
    def search_symbol_data(self, symbol_type = None, domain = None):
        return super().search_symbol_data(symbol_type, domain)
    
    def get_symbol_model(self):
        return super().get_symbol_model()
    
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

    def resolve_enum_symbol(self, symbol_ref: str) -> str:
        """
        硬编码解析枚举符号引用
        格式: intervention.ENUM_NAME 或 intervention.ENUM_CLASS.ENUM_VALUE.value
        """
        if not symbol_ref.startswith("intervention."):
            return symbol_ref
        
        # 移除 "intervention." 前缀
        enum_path = symbol_ref.split(".", 1)[1]
        
        # 硬编码枚举值映射（简单枚举名）
        enum_mapping = {
            "USER_ACCEPTED": "INVEvent.USER_ACCEPTED.value",
            "USER_REJECTED": "INVEvent.USER_REJECTED.value", 
            "INTERVENTION_CREATED": "INVEvent.INTERVENTION_CREATED.value",
            "END_INTERVENTION": "INV_Special_States.END_INTERVENTION.value",
            "ACCEPTED_CONTRACT": "INV_Special_States.ACCEPTED_CONTRACT.value"
        }
        
        # 检查是否是简单枚举名
        if enum_path in enum_mapping:
            return f"ti.features.intervention.model.model.{enum_mapping[enum_path]}"
        
        # 检查是否是复杂枚举路径格式：ENUM_CLASS.ENUM_VALUE.value
        if enum_path.endswith(".value") and enum_path.count(".") >= 2:
            # 格式：INV_View_ID.POST_EAT_WASTE.value
            full_enum_path = f"ti.features.intervention.model.model.{enum_path}"
            return full_enum_path
        
        return symbol_ref
    
    def regist_symbol_path(self, symbol_model):
        return super().regist_symbol_path(symbol_model)