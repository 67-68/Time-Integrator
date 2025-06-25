from PyQt6.QtWidgets import QWidget,QVBoxLayout

from QtUI.widgets.other.BasicButton import BasicButton


class LeftToolFrame(QWidget):
    def __init__(self, fatherFrame = None,buttons = None):
        super().__init__(fatherFrame) #引用父类方法，创建一个Frame
        self.setStyleSheet("background-color: #A9B0B3;") #修改颜色
        
        self.buttons = []

        #  ------ 创建排版器 ------
        self.buttonLayout = QVBoxLayout()
        
        #  ------ 设置layout ------
        self.setLayout(self.buttonLayout)
        
    def coverToolButtons(self,buttons):        
        #  ------ 开始排版按钮 ------
        if buttons != []:
            for button in buttons:
                btn = BasicButton(self)
                btn.setText(button["text"])
                btn.clicked.connect(button["clicked"])  # 用信号槽绑定
                self.buttonLayout.addWidget(btn)

        #一个按钮的列表什么的就不管了...想不到怎么用