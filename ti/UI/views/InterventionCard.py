from PyQt6.QtWidgets import QWidget

from ti.UI.rawUI.ui_InterventionCard import Ui_interventionWidget
from ti.UI.widgets.other.BasicButton import BasicButton

class InterventionCard(QWidget):
    def __init__(
        self,
        title: str,
        choices: list,
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
        
        self.buttons = {}
        
        for choice in choices:
            text = choices[choice]
            id = choice
            
            self.buttons[id] = BasicButton(self.ui.choiceWidget)
            self.buttons[id].setText(text)
            
            self.ui.choiceLayout.addWidget(self.buttons[id])
            
            
        

        