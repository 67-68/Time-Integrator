from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional


class InsightPathRegister(ISymbolPathRegister):
    """
    Path register for insight feature functions and classes
    """
    
    def __init__(self):
        self._symbols: Dict[str, SymbolModel] = {}
        self.load_data()
    
    @property
    def domain(self) -> str:
        return "insight"
    
    @property
    def enum_mapping(self) -> str:
        return {}
    
    @property
    def class_file_path(self) -> str:
        return "ti/features/insight/model/data/insight_classes.yaml"
    
    @property
    def class_method_file_path(self) -> str:
        return "ti/features/insight/model/data/insight_class_methods.yaml"
    
    @property
    def function_file_path(self) -> str:
        return "ti/features/insight/model/data/insight_functions.yaml"
    
    @property
    def enum_file_path(self) -> str:
        return "ti/features/insight/model/data/insight_enums.yaml"
    
    def regist_symbol_path(self, symbol_model):
        return super().regist_symbol_path(symbol_model)
    
    def get_symbol_path(self, symbol_id):
        return super().get_symbol_path(symbol_id)
    
    def search_symbol_data(self):
        return super().search_symbol_data()
    
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