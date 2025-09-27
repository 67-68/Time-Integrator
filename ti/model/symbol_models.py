from dataclasses import dataclass
from enum import Enum

class SymbolType(Enum):
    CLASS_METHOD = "class_method"
    FUNCTION = "function"
    CLASS = "class"
    ENUM_CLASS = "enum_class"

@dataclass
class SymbolModel:
    """
    这个类用来存储所有symbol的基本数据
    """
    symbol_type: SymbolType
    symbol_path: str
    symbol_domain: str
    symbol_name: str = None