from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel

class BottomInfoFrame(QWidget):
    def __init__(self, master = None):
        super().__init__(master)
        self.setStyleSheet("background-color: #F4F4F4;")
        
        #  ------ 错误信息封装 ------
        self.infoLabel = QLabel(self,text = "error will show in here")
        
        
        #  ------ 设置布局器 ------
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.infoLabel)
        self.setLayout(self.layout)
        
        
    def showError(self,errorText):
        self.infoLabel.setText(errorText)
        
        
        
        
        
    
