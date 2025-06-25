import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class TimeIntegrator(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        # 你可以在这里写全局配置，比如字体、样式等

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Integrator")
        # 这里添加一个标签，作为主界面内容
        label = QLabel("Hello, PyQt6! 这里是主窗口。")
        self.setCentralWidget(label)

# 3. 主程序入口
if __name__ == "__main__":
    app = MyApplication(sys.argv)    # 创建应用对象
    window = MainWindow()            # 创建主窗口对象
    window.show()                    # 显示窗口
    sys.exit(app.exec())             # 进入事件循环