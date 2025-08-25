from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from ti.UI.rawUI.ui_InterventionCard import Ui_interventionWidget
from ti.UI.widgets.other.BasicButton import BasicButton

class InterventionCard(QWidget):
    user_promise = pyqtSignal(dict)
    # 会包含self和detector
    
    user_giveUp = pyqtSignal(dict)
    # 还没想好放什么
    
    def __init__(
        self,
        title: str,
        choices: list,
        id,
        parent = None
        ):
        """_summary_

        Args:
            title (str): 干涉的标题
            choice (list): 干涉的选项
        """
        super().__init__(parent)
        self.ui = Ui_interventionWidget()
        self.ui.setupUi(self)
        
        # 初始化外观
        self.ui.title.setText(title)
        
        self.id = id
        
        self.buttons = {}
        
        for choice in choices:
            text = choices[choice]
            id = choice
            
            self.buttons[id] = BasicButton(self.ui.choiceWidget)
            self.buttons[id].setText(text)
            
            self.ui.choiceLayout.addWidget(self.buttons[id])
        
        # 连接信号
        self.buttons["choice_giveUp"].clicked.connect(self._on_giveUp_clicked)
        self.buttons["choice_accept"].clicked.connect(self._on_user_promised)
        
    def _on_giveUp_clicked(self):
        pass
    
    def _on_user_promised(self):
        pack = {
            "ui": self,
            "detector": self.detector,
            "id":self.id,
            "state": self.state
        }
        
        self.user_promise.emit(pack)
    
    def deleteButton(self,name):
        self.ui.choiceLayout.removeWidget(self.buttons[name])
    
    def addWidget_inButtonPlace(self,widget):
        self.ui.choiceLayout.addWidget(widget)
        
        
        
            
            
        

        