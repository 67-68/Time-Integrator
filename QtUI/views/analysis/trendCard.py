from QtUI.rawUI.ui_rawDailyTrendCard import Ui_trendCard
from PyQt6.QtWidgets import QWidget

class trendCard(QWidget):
    def __init__(self,
            parent = None
            #这里放需要输入进来的变量
            ):
        super().__init__(parent)
        
        self.TC = Ui_trendCard()
        self.TC.setupUi(self)
        
        #这里手动填充各项数据
        
        
        