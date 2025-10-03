from enum import Enum, auto
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QTabWidget
from ti.view.BasicWidget import BasicWidget

class CaptureView(BasicWidget):
    """
    CaptureView 是 Capture 插件的主 UI 容器，
    使用 Tab 布局组织不同的功能视图。
    """
    # 1. 定义一个枚举来区分 Tab 组
    class TabType(Enum):
        CONTEXT_SELECTION = auto()
        ITEM_DISPLAY = auto()
        ITEM_EDITOR = auto()

    # 2. 使用一个统一的信号
    tab_changed = pyqtSignal(TabType, str)  # 发射 (Tab组类型, Tab名称)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._presenter_to_widget_map: dict[str, QTabWidget] = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI布局"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # 创建左侧垂直布局（占据1/2宽度）
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        # 创建右侧布局（占据1/2宽度）
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        # 将左右布局添加到主布局
        self.main_layout.addLayout(self.left_layout, 1)  # 左侧占据1/2
        self.main_layout.addLayout(self.right_layout, 1)  # 右侧占据1/2

        # 创建 TabWidget
        self.context_selection_tab_widget = self._create_tab_widget(self.TabType.CONTEXT_SELECTION)
        self.item_display_tab_widget = self._create_tab_widget(self.TabType.ITEM_DISPLAY)
        self.item_editor_tab_widget = self._create_tab_widget(self.TabType.ITEM_EDITOR)

        # 将 TabWidget 添加到布局
        self.left_layout.addWidget(self.context_selection_tab_widget, 1)
        self.left_layout.addWidget(self.item_display_tab_widget, 1)
        self.right_layout.addWidget(self.item_editor_tab_widget)
        
    def _create_tab_widget(self, tab_type: TabType) -> QTabWidget:
        """辅助函数：创建一个 TabWidget 并连接其信号"""
        tab_widget = QTabWidget()
        # 使用 lambda 或 functools.partial 来传递额外参数
        tab_widget.currentChanged.connect(lambda index, t=tab_type: self._on_tab_changed(t, index))
        return tab_widget

    def add_tab(self, tab_type: TabType, widget: QWidget, name: str):
        """向指定的 Tab 组添加一个 Tab"""
        # 3. 统一的 Tab 添加方法
        target_widget = None
        if tab_type == self.TabType.CONTEXT_SELECTION:
            target_widget = self.context_selection_tab_widget
        elif tab_type == self.TabType.ITEM_DISPLAY:
            target_widget = self.item_display_tab_widget
        elif tab_type == self.TabType.ITEM_EDITOR:
            target_widget = self.item_editor_tab_widget
        
        if target_widget:
            target_widget.addTab(widget, name)
            # 4. 维护 presenter_name -> QTabWidget 的映射
            self._presenter_to_widget_map[name] = target_widget

    def switch_to_tab(self, presenter_name: str) -> bool:
        """高效地切换到指定名称的 Presenter 所在的 Tab"""
        # 5. O(1) 查找，不再需要循环
        target_widget = self._presenter_to_widget_map.get(presenter_name)
        if not target_widget:
            print(f"未找到名为 {presenter_name} 的 Tab")
            return False

        for i in range(target_widget.count()):
            if target_widget.tabText(i) == presenter_name:
                target_widget.setCurrentIndex(i)
                print(f"成功切换到 Tab: {presenter_name}")
                return True
        return False

    def _on_tab_changed(self, tab_type: TabType, index: int):
        """统一处理所有 TabWidget 的 currentChanged 信号"""
        # 6. 一个槽函数处理所有信号
        if index == -1:
            return
            
        target_widget = None
        if tab_type == self.TabType.CONTEXT_SELECTION:
            target_widget = self.context_selection_tab_widget
        elif tab_type == self.TabType.ITEM_DISPLAY:
            target_widget = self.item_display_tab_widget
        elif tab_type == self.TabType.ITEM_EDITOR:
            target_widget = self.item_editor_tab_widget
        
        if target_widget:
            tab_name = target_widget.tabText(index)
            self.tab_changed.emit(tab_type, tab_name)

    # 移除了所有 setup_ui 之外的 add_*_view, add_*_tab 方法
    # 移除了 _on_*_tab_changed 三个独立方法
    # 移除了 _set_initial_active_state (这个职责更适合 Presenter)
    # 移除了 _clear_layout (如果确实需要，可以保留