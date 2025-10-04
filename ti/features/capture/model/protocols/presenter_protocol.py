from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class IPresenter(Protocol):
    def get_view(self):
        pass