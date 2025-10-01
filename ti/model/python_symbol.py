import importlib
from typing import Any, Callable


class PythonSymbol:
    """
    一个自定义类型，Pydantic会知道如何处理它。
    它期望字符串为完整路径
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field) -> Callable | type:
        """
        这就是"解析"的魔法所在！
        当Pydantic遇到一个需要被解析为PythonSymbol的字段时，
        它会自动调用这个方法。
        """
        if not isinstance(value, str):
            raise TypeError('String required for a Python symbol')

        # === 你的SymbolResolver的核心逻辑，现在住在这里！ ===
        try:
            module_path, symbol_name = value.rsplit('.', 1)
            module = importlib.import_module(module_path)
            symbol = getattr(module, symbol_name)
            print(f"Successfully resolved '{value}' to {symbol}")
            return symbol
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Could not resolve symbol: {value}") from e
        