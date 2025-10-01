from typing import Protocol, runtime_checkable

from ti.view.BasicFrame import BasicFrame

@runtime_checkable
class SelectionProtocol(Protocol):
    def create_selection_view(self) -> BasicFrame:
        pass