"""
这个函数用来存放所有用来替换View的Protocol
如果策略满足这些protocol就可以作为一个备选策略
"""


from typing import Protocol, runtime_checkable

from ti.features.capture_test.model.protocols.presenter_protocol import IPresenter
from ti.view.BasicFrame import BasicFrame


@runtime_checkable
class IContextSelection(Protocol):
    def create_context_selection_presenter(self) -> type[IPresenter]: #返回一个Presenter, 内部有get_view供插槽使用
        pass

@runtime_checkable    
class IItemDisplay(Protocol):
    def create_item_display_presenter(self) -> type[IPresenter]:
        pass

@runtime_checkable
class IItemEditor(Protocol):
    def create_item_editor_presenter(self) -> type[IPresenter]:
        pass
