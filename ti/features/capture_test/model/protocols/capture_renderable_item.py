from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass
class RenderableItemModel:
    """
    可渲染物的Data Model
    Protocol签名的结果的东西
    以及运行时存储的状态
    """
    base_model: BaseModel # 数据模型的Data Model
    factory: Any # 数据模型的渲染工厂
    item_displayable_list: list[str] # 签名，表示可以在哪里展示
    item_editorable_list: list[str] # 签名 表示可以在哪里修改
    
    
    