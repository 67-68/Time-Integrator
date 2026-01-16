# 建议放在一个新文件，如 ti/presenters/presenter_group_manager.py
from typing import TypeVar, Generic, Callable

# 使用 TypeVar 来创建泛型类，使其能管理任何类型的 Presenter
T = TypeVar('T')

class PresenterGroupManager(Generic[T]):
    """管理一组功能相似的 Presenter"""
    def __init__(self, presenters: list[T]):
        self.presenters: dict[str, T] = {p.name: p for p in presenters}
        self.active: T | None = None

    def initialize_all(self) -> None:
        """初始化组内所有 Presenter"""
        for presenter in self.presenters.values():
            presenter.initialize()

    def connect_all(self, slot: Callable) -> None:
        """将组内所有 Presenter 的特定信号连接到同一个槽函数"""
        # 注意: 这假设所有 Presenter 都有一个统一的信号名，
        # 如果信号名不同，则需要更复杂的逻辑
        for presenter in self.presenters.values():
            # 示例信号，需要根据实际情况修改
            if hasattr(presenter, 'selection_condition_changed'):
                presenter.selection_condition_changed.connect(slot)
            elif hasattr(presenter, 'item_selected'):
                presenter.item_selected.connect(slot)

    def get(self, name: str) -> T | None:
        return self.presenters.get(name)

    def values(self):
        return self.presenters.values()

    def __getitem__(self, key):
        return self.presenters[key]