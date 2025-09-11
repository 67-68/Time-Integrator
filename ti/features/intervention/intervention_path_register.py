from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional


class InterventionPathRegister(ISymbolPathRegister):
    """
    Path register for intervention feature functions and classes
    """
    
    def __init__(self):
        self._symbols: Dict[str, SymbolModel] = {}
        self.load_data()
    
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