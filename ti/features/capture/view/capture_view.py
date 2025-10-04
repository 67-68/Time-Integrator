from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QTabWidget
from ti.model.action_unit import ActionUnit
from ti.view.BasicWidget import BasicWidget


class CaptureView(BasicWidget):
    """
    CaptureWidget是capture插件的主要UI组件
    整合日历、记录选择、智能输入等子功能
    """

    # 定义Tab变化信号
    context_selection_tab_changed = pyqtSignal(str)  # 发射tab名称
    item_display_tab_changed = pyqtSignal(str)       # 发射tab名称
    item_editor_tab_changed = pyqtSignal(str)        # 发射tab名称

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        # 创建主水平布局
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

        # 创建三个TabWidget分别用于不同区域
        self.context_selection_tab_widget = QTabWidget()
        self.item_display_tab_widget = QTabWidget()
        self.item_editor_tab_widget = QTabWidget()

        # 连接TabWidget信号
        self.context_selection_tab_widget. currentChanged.connect(self._on_context_selection_tab_changed)
        self.item_display_tab_widget.currentChanged.connect(self._on_item_display_tab_changed)
        self.item_editor_tab_widget.currentChanged.connect(self._on_item_editor_tab_changed)

        # 将TabWidget添加到布局
        self.add_context_selection_view(self.context_selection_tab_widget)
        self.add_item_display_view(self.item_display_tab_widget)
        self.add_item_editor_view(self.item_editor_tab_widget)
    
    def add_context_selection_view(self, context_selection_view):
        """添加上下文选择视图到左上角（左侧1/4）"""
        context_selection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_layout.addWidget(context_selection_view, 1)  # 占据左侧垂直布局的1/2高度

    def add_item_display_view(self, item_display_view):
        """添加项目显示视图到左下角（左侧1/4）"""
        item_display_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_layout.addWidget(item_display_view, 1)  # 占据左侧垂直布局的1/2高度

    def add_item_editor_view(self, item_editor_view):
        """添加项目编辑视图到右侧（右侧1/2）"""
        item_editor_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.right_layout.addWidget(item_editor_view)

    def add_tab_widget(self, tab_widget):
        """添加TabWidget到主布局"""
        tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 清空现有布局并添加TabWidget
        self._clear_layout()
        self.main_layout.addWidget(tab_widget)

    def add_context_selection_tab(self, widget, name):
        """添加上下文选择Tab"""
        self.context_selection_tab_widget.addTab(widget, name)

    def add_item_display_tab(self, widget, name):
        """添加项目显示Tab"""
        self.item_display_tab_widget.addTab(widget, name)

    def add_item_editor_tab(self, widget, name):
        """添加项目编辑Tab"""
        self.item_editor_tab_widget.addTab(widget, name)

    def switch_to_tab(self, presenter_name):
        """切换到指定名称的presenter tab"""
        # 尝试在Context Selection TabWidget中查找
        for i in range(self.context_selection_tab_widget.count()):
            tab_name = self.context_selection_tab_widget.tabText(i)
            if tab_name == presenter_name:
                self.context_selection_tab_widget.setCurrentIndex(i)
                print(f"切换到Context Selection tab: {presenter_name}")
                return True

        # 尝试在Item Display TabWidget中查找
        for i in range(self.item_display_tab_widget.count()):
            tab_name = self.item_display_tab_widget.tabText(i)
            if tab_name == presenter_name:
                self.item_display_tab_widget.setCurrentIndex(i)
                print(f"切换到Item Display tab: {presenter_name}")
                return True

        # 尝试在Item Editor TabWidget中查找
        for i in range(self.item_editor_tab_widget.count()):
            tab_name = self.item_editor_tab_widget.tabText(i)
            if tab_name == presenter_name:
                self.item_editor_tab_widget.setCurrentIndex(i)
                print(f"切换到Item Editor tab: {presenter_name}")
                return True

        print(f"未找到名为 {presenter_name} 的tab")
        return False

    def _on_context_selection_tab_changed(self, index):
        """处理Context Selection Tab变化事件"""
        if index == -1:
            return
        tab_name = self.context_selection_tab_widget.tabText(index)
        self.context_selection_tab_changed.emit(tab_name)

    def _on_item_display_tab_changed(self, index):
        """处理Item Display Tab变化事件"""
        if index == -1:
            return
        tab_name = self.item_display_tab_widget.tabText(index)
        self.item_display_tab_changed.emit(tab_name)

    def _on_item_editor_tab_changed(self, index):
        """处理Item Editor Tab变化事件"""
        if index == -1:
            return
        tab_name = self.item_editor_tab_widget.tabText(index)
        self.item_editor_tab_changed.emit(tab_name)

    def _clear_layout(self):
        """清空现有布局"""
        # 清空左侧布局
        while self.left_layout.count():
            child = self.left_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 清空右侧布局
        while self.right_layout.count():
            child = self.right_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
