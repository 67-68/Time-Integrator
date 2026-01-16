from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from ti.features.capture.service.capture_factory_interface import ICaptureRenderer


@dataclass
class RenderableItemModel:
    """
    可渲染物的Data Model
    Protocol签名的结果的东西
    以及运行时存储的状态
    """
    item_name: str # Item的名字
    base_model: BaseModel # 数据模型的Data Model
    renderer: ICaptureRenderer # 数据模型的渲染工厂, 需要实例
    item_displayable_list: list[str] # 签名，表示可以在哪里展示
    item_editorable_list: list[str] # 签名 表示可以在哪里修改
    
    
    