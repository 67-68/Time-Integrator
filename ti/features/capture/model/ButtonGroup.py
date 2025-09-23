from PyQt6.QtWidgets import QScrollArea, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from ti.view.BasicButton import BasicButton


class ButtonGroup(QScrollArea):
    # 信号定义
    save_requested = pyqtSignal()
    new_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_direction = Qt.Orientation.Vertical
        self._delete_click_count = 0  # 删除按钮点击计数器
        self._create_default_buttons()
    
    def _setup_ui(self):
        self.setWidgetResizable(True)
        
        
        self.container_widget = QWidget()
        self.vertical_layout = QVBoxLayout(self.container_widget)
        self.horizontal_layout = QHBoxLayout(self.container_widget)
        
        
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        
        
        self.horizontal_layout.setParent(None)
        self.container_widget.setLayout(self.vertical_layout)
        
        self.setWidget(self.container_widget)
    
    def register_button(self, display_text, callback=None):
        button = BasicButton(self.container_widget)
        button.setText(display_text)
        
        if callback:
            button.clicked.connect(callback)
        
        
        if self._current_direction == Qt.Orientation.Vertical:
            self.vertical_layout.addWidget(button)
        else:
            self.horizontal_layout.addWidget(button)
        
        return button
    
    def set_scroll_direction(self, direction):
        if direction not in [Qt.Orientation.Vertical, Qt.Orientation.Horizontal]:
            raise ValueError("{/ Qt.Orientation.Vertical Qt.Orientation.Horizontal")
        
        if direction == self._current_direction:
            return
        
        
        self._current_direction = direction
        
        
        buttons = []
        if direction == Qt.Orientation.Vertical:
        
            while self.horizontal_layout.count():
                item = self.horizontal_layout.takeAt(0)
                if item.widget():
                    buttons.append(item.widget())
        
            self.container_widget.setLayout(self.vertical_layout)
        
            for button in buttons:
                self.vertical_layout.addWidget(button)
        else:
        
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    buttons.append(item.widget())
        
            self.container_widget.setLayout(self.horizontal_layout)
        
            for button in buttons:
                self.horizontal_layout.addWidget(button)
    
    def clear_buttons(self):
        
        if self._current_direction == Qt.Orientation.Vertical:
            while self.vertical_layout.count():
                item = self.vertical_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            while self.horizontal_layout.count():
                item = self.horizontal_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
    
    def get_scroll_direction(self):
        
        return self._current_direction
    
    def _create_default_buttons(self):
        """创建默认按钮：保存、新建和删除"""
        # 保存按钮
        save_btn = self.register_button("保存", self._on_save_clicked)
        
        # 新建按钮
        new_btn = self.register_button("新建", self._on_new_clicked)
        
        # 删除按钮
        delete_btn = self.register_button("删除", self._on_delete_clicked)
    
    def _on_save_clicked(self):
        """保存按钮点击处理"""
        self.save_requested.emit()
    
    def _on_new_clicked(self):
        """新建按钮点击处理"""
        self.new_requested.emit()
    
    def _on_delete_clicked(self):
        """删除按钮点击处理"""
        self._delete_click_count += 1
        
        if self._delete_click_count >= 2:
            # 第二次点击，发射删除信号并重置计数器
            self.delete_requested.emit()
            self._reset_delete_count()
    
    def _reset_delete_count(self):
        """重置删除计数器"""
        self._delete_click_count = 0
    
    def reset_delete_count(self):
        """公开方法：重置删除计数器"""
        self._reset_delete_count()