from enum import Enum
from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional


class CorePathRegister(ISymbolPathRegister):
    """
    Path register for model feature functions and classes
    """
    
    def __init__(self):
        self._symbols: Dict[str, SymbolModel] = {}
        self.load_data()
    
    @property
    def domain(self) -> str:
        return "model"
    
    @property
    def class_file_path(self) -> str:
        return "ti/model/data/model_classes.yaml"
    
    @property
    def class_method_file_path(self) -> str:
        return "ti/model/data/model_class_methods.yaml"
    
    @property
    def function_file_path(self) -> str:
        return "ti/model/data/model_functions.yaml"
    
    @property
    def enum_file_path(self) -> str:
        return "ti/model/data/model_enums.yaml"
    
    def regist_symbol_path(self, symbol_model: SymbolModel) -> None:
        """
        Register a symbol path
        """
        symbol_id = f"{symbol_model.symbol_type.value}:{symbol_model.symbol_path}"
        self._symbols[symbol_id] = symbol_model
    
    def get_symbol_path(self, symbol_id: str) -> Optional[SymbolModel]:
        """
        Get symbol by id
        """
        # 首先检查硬编码的枚举映射
        enum_mapping = {
            "TODAY": "ti.model.duration.Duration.TODAY.value",
            "TO_TOMORROW": "ti.model.duration.Duration.TO_TOMORROW.value", 
            "THIS_WEEK": "ti.model.duration.Duration.THIS_WEEK.value"
        }
        
        if symbol_id in enum_mapping:
            # 返回枚举符号的SymbolModel
            return SymbolModel(
                symbol_type=SymbolType.ENUM_CLASS,
                symbol_path=enum_mapping[symbol_id],
                symbol_domain="model"
            )
        
        return self._symbols.get(symbol_id)
    
    def search_symbol_data(self, symbol_type: Optional[SymbolType] = None, 
                          domain: Optional[str] = None) -> List[SymbolModel]:
        """
        Search symbols by type and/or domain
        """
        results = []
        for symbol in self._symbols.values():
            if symbol_type and symbol.symbol_type != symbol_type:
                continue
            if domain and symbol.symbol_domain != domain:
                continue
            results.append(symbol)
        return results
    
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
    
    def _load_from_file(self, file_path: str, key: str) -> None:
        """
        Load data from a specific YAML file
        """
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                
            if data and key in data:
                for item in data[key]:
                    if not isinstance(item,str):
                    
                        symbol = SymbolModel(
                            symbol_type=SymbolType(item['symbol_type']),
                            symbol_path=item['symbol_path'],
                            symbol_domain=item['symbol_domain']
                        )
                        self.regist_symbol_path(symbol)
                        
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
        except Exception as e:
            print(f"Error loading symbol data from {file_path}: {e}")

    def resolve_enum_symbol(self, symbol_ref: str) -> str:
        """
        硬编码解析枚举符号引用
        格式: model.ENUM_NAME
        """
        if not symbol_ref.startswith("model."):
            return symbol_ref
        
        enum_name = symbol_ref.split(".", 1)[1]
        
        # 硬编码枚举值映射
        enum_mapping = {
            "TODAY": "Duration.TODAY.value",
            "TO_TOMORROW": "Duration.TO_TOMORROW.value", 
            "THIS_WEEK": "Duration.THIS_WEEK.value"
        }
        
        if enum_name in enum_mapping:
            return f"ti.model.duration.{enum_mapping[enum_name]}"
        
        return symbol_ref