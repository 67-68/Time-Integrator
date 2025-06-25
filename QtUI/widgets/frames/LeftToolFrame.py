from PyQt6.QtWidgets import QWidget,QVBoxLayout

from QtUI.widgets.other.BasicButton import BasicButton


class LeftToolFrame(QWidget):
    def __init__(self, fatherFrame = None,buttons = None):
        super().__init__(fatherFrame) #引用父类方法，创建一个Frame
        self.setStyleSheet("background-color: #A9B0B3;") #修改颜色
        
        self.buttons = []

        #  ------ 创建排版器 ------
        self.buttonLayout = QVBoxLayout()
        
        
        #  ------ 开始排版按钮 ------
        for label, cmd in buttons:
            btn = BasicButton(self, text=label, command=cmd)
            self.buttonLayout.addWidget(btn)
            self.buttons.append(btn)
            

        #  ------ 设置layout ------
        self.setLayout(self.buttonLayout)