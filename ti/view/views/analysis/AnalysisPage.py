from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from ti.view.views.analysis.trendCard import InsightCard
from ti.presenters.InsightCardPresenter import InsightCardPresenter
from ti.services.formatter import FormatService
from ti.view.widgets.pages.BasicFrame import BasicFrame
from ti.view.rawUI.ui_rawAnalysisPage import Ui_analysisPage
from ti.core.eventBus import EventBus
from ti.services.sessionCache import SessionCache

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
        
        # 卡片逻辑类存储
        self.currentLogicCards = {}
    
    def add_cards(
        self,
        cards,
        FS: FormatService,
        bus: EventBus,
        cache: SessionCache
        ):
        """_summary_

        Args:
            cards (list of dict): 卡片信息列表
        """
        # ------ 创建类，生成卡片 ------
        currentCards = {}
        
        
        for idx, card_data in enumerate(cards): # card_data也就是formatter处理后的pre_data
            data = FS.format_card(card_data)
            card = InsightCard(data, parent=self.CA) 
            
            bus.publish("insight_card_ui_created",(card,cache))
            
            currentCards[idx] = card
            cardPresenter = InsightCardPresenter(currentCards[idx])
            self.currentLogicCards[idx] = cardPresenter
            
            self.cards.append(currentCards[idx])     # 保存引用，防止被垃圾回收
            self.CA.layout().addWidget(self.cards[idx])            # 加入垂直布局，自上而下显示
            
        """
        在这里，关于Intervention,首先按理来说它可以正确传递到这里
        但如何正确的生成Intervention呢？我觉得可以在format card的时候把Intervention单独领出来作为一个key
        然后它是一个dict包含Intervention Card的信息
        然后在外部判断创建Intervention Card, 作为依赖输入trend card
        """