"""
这个函数用来存放所有用来替换View的Protocol
如果策略满足这些protocol就可以作为一个备选策略
"""


from typing import Protocol, runtime_checkable

from ti.core.eventBus import EventBus
from ti.features.capture_test.model.protocols.presenter_protocol import IPresenter
from ti.features.capture_test.presenter.context_selection_presenter_interface import IContextSelectionPresenter
from ti.features.capture_test.presenter.item_display_presenter_interface import IItemDisplayPresenter
from ti.features.capture_test.presenter.item_editor_presenter_interface import IItemEditorPresenter
from ti.services.dataService import DataService
from ti.view.BasicFrame import BasicFrame


@runtime_checkable
class IContextSelection(Protocol):
    def create_context_selection_presenter(self) -> type[IContextSelectionPresenter]: #返回一个Presenter, 内部有get_view供插槽使用
        pass

@runtime_checkable    
class IItemDisplay(Protocol):
    def create_item_display_presenter(self) -> type[IItemDisplayPresenter]:
        pass

@runtime_checkable
class IItemEditor(Protocol):
    def create_item_editor_presenter(self) -> type[IItemEditorPresenter]:
        pass

@runtime_checkable
class ICaptureView(Protocol):
    def create_capture_view(
        self,
        context_selection_presenter: IContextSelection,
        item_display_presenter: IItemDisplay,
        item_editor_presenter: IItemEditor,
        data_service: DataService,
        bus: EventBus
    ):
        pass