from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from ti.UI.presenters.formatter import format_card
from ti.UI.rawUI.ui_rawAnalysisPage import Ui_analysisPage
from ti.UI.views.analysis.trendCard import TrendCard
from ti.UI.widgets.pages.BasicFrame import BasicFrame



class AnalysisPage(BasicFrame):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self,parent = None):
        super().__init__(parent)
        
        self.AP = Ui_analysisPage()
        self.AP.setupUi(self)
        self.AP.cardsScroll.setWidgetResizable(True)
        
        self.AP.pageSwitchFrameBase.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        self.cards = []
        self.CA = self.AP.cardsArea
        
        # 为 cardsArea 设置一个垂直布局，使卡片按照自上而下顺序排列
        self.CA_layout = QVBoxLayout()
        self.CA.setLayout(self.CA_layout)
        
    
    def add_cards(self,cards):
        """_summary_

        Args:
            cards (list of dict): 卡片信息列表
        """
        # ------ 创建类，生成卡片 ------
        for idx, card_data in enumerate(cards):
            data = format_card(card_data)
            self.cards.append(TrendCard(data, parent=self.CA))     # 保存引用，防止被垃圾回收
            self.CA.layout().addWidget(self.cards[idx])            # 加入垂直布局，自上而下显示