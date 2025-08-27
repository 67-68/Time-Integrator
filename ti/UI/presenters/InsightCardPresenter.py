from PyQt6.QtCore import QObject

from ti.UI.views.analysis.trendCard import TrendCard
from ti.UI.widgets.other.BasicButton import BasicButton

class InsightCardPresenter(QObject):
    def __init__(
        self,
        card_ui: TrendCard,
        parent = None
    ):
        """_summary_
        卡片逻辑类，负责管理卡片的UI
        Args:
            parent (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(parent)
        self.ui = card_ui
        
        # if intervention:
        #     self.intervention_ui = intervention
        #     self.intervention_connect()
        
        # self.IS = IS

    
        
    def intervention_connect(self):
        button_accpet: BasicButton = self.intervention_ui.buttons["choice_accept"]
        self.intervention_ui.user_promise.connect(lambda data: self.create_intervention(data)) #问题出在这里，信号没有传过来
        
        button_giveUp: BasicButton = self.intervention_ui.buttons["choice_giveUp"]
        button_giveUp.clicked.connect(self.giveUp)
        
    def create_intervention(
        self,
        data # 从InterventionCard过来的
        ):
        self.IS.create_intervention(data) #为什么这里没有继续？
    
    def giveUp(self):
        pass
        