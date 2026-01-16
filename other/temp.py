import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# =======================================================
# 1. 模拟你的数据模型 (Dataclasses)
#    在真实项目中，你会从你的model文件中导入它们
# =======================================================
from dataclasses import dataclass, field
from typing import List

@dataclass
class ActionUnit:
    name: str
    time_range: str

@dataclass
class ContextBlock:
    name: str
    color: str # e.g., "#E6F7FF" (a light blue)
    action_units: List[ActionUnit] = field(default_factory=list)

# =======================================================
# 2. 那个核心的“容器”Widget (The "Magic" Happens Here)
# =======================================================
class ContextContainerWidget(QWidget):
    """
    这个Widget，就是你设想的那个“框框”。
    它接收一个ContextBlock的数据，并把自己渲染成对应的样子。
    """
    def __init__(self, context_data: ContextBlock, parent=None):
        super().__init__(parent)
        self.context_data = context_data

        # --- 核心的UI和布局 ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10) # 内部留一点边距
        self.main_layout.setSpacing(5)

        # --- 设置“染色”和“圆角边框” ---
        # 这就是实现“框框”效果的关键！
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.context_data.color};
                border-radius: 8px;
            }}
        """)
        self.setAutoFillBackground(True) # 确保背景色被填充

        self._setup_ui()

    def _setup_ui(self):
        # 1. 创建并添加标题
        title_label = QLabel(f"Context: {self.context_data.name}")
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        self.main_layout.addWidget(title_label)

        # 2. 循环创建并添加嵌套的ActionUnit Widgets
        if not self.context_data.action_units:
            no_actions_label = QLabel(" (No actions in this context)")
            no_actions_label.setStyleSheet("color: gray;")
            self.main_layout.addWidget(no_actions_label)
        else:
            for au_data in self.context_data.action_units:
                au_widget = self._create_au_widget(au_data)
                self.main_layout.addWidget(au_widget)
    
    def _create_au_widget(self, au_data: ActionUnit) -> QWidget:
        """
        一个简单的工厂方法，用来创建代表ActionUnit的UI。
        在真实应用中，这可能是另一个专门的类。
        """
        # 为了让ActionUnit看起来也像一个独立的卡片，我们再次使用容器
        au_container = QWidget()
        au_layout = QVBoxLayout(au_container)
        au_layout.setContentsMargins(5, 5, 5, 5)
        
        # 我们可以给它一个不同的、更浅的背景色，或者一个边框
        au_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 4px;
            }
        """)
        au_container.setAutoFillBackground(True)
        
        name_label = QLabel(f"Action: {au_data.name}")
        time_label = QLabel(f"Time: {au_data.time_range}")
        
        au_layout.addWidget(name_label)
        au_layout.addWidget(time_label)
        
        return au_container

# =======================================================
# 3. 主测试窗口
# =======================================================
class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Context Container Test")
        self.setGeometry(300, 300, 400, 500)

        # --- 准备模拟数据 ---
        context1 = ContextBlock(
            name="上午学习",
            color="#E6F7FF", # 淡蓝色
            action_units=[
                ActionUnit(name="阅读论文", time_range="09:00 - 10:30"),
                ActionUnit(name="写代码", time_range="10:30 - 12:00")
            ]
        )
        
        context2 = ContextBlock(
            name="午休",
            color="#F6FFED", # 淡绿色
            action_units=[
                ActionUnit(name="吃饭", time_range="12:15 - 12:45"),
                ActionUnit(name="刷手机 (Waste)", time_range="12:45 - 13:15")
            ]
        )
        
        context3 = ContextBlock(
            name="会议",
            color="#FFF2E8", # 淡橙色
            action_units=[] # 测试没有action的情况
        )

        # --- 设置主布局 ---
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(15)
        self.setCentralWidget(central_widget)

        # --- 创建并添加我们的“容器”Widgets ---
        container1_widget = ContextContainerWidget(context1)
        container2_widget = ContextContainerWidget(context2)
        container3_widget = ContextContainerWidget(context3)
        
        self.main_layout.addWidget(container1_widget)
        self.main_layout.addWidget(container2_widget)
        self.main_layout.addWidget(container3_widget)

# =======================================================
# 4. 运行程序
# =======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())