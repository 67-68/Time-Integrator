from typing import Protocol, runtime_checkable

from ti.features.capture_test.model.protocols.capture_renderable_item import RenderableItemModel

@runtime_checkable
class IRenderableItemProtocol(Protocol):
    """
    定义了一个协议
    用来获取所有的RenderableItemDataclass

    Args:
        Protocol (_type_): _description_
    """
    @property
    def capture_data_model(self) -> RenderableItemModel:
        pass