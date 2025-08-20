from PyQt6.QtCore import QObject

from ti.UI.views.InterventionCard import InterventionCard
from ti.UI.views.analysis.trendCard import TrendCard
from ti.UI.widgets.other.BasicButton import BasicButton
from ti.services.interventionService import InterventionService

class InsightCardPresenter(QObject):
    def __init__(
        self,
        card_ui: TrendCard,
        IS: InterventionService,
        intervention: InterventionCard = None,
        parent = None
    ):
        """_summary_
        卡片逻辑类，负责管理卡片的UI
        Args:
            parent (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(parent)
        self.ui = card_ui
        
        if intervention:
            self.intervention_ui = intervention
        
        self.IS = IS
        
        # 信号接收
    
        
    def intervention_connect(self):
        button_accpet: BasicButton = self.intervention_ui.buttons["choice_accept"]
        self.intervention_ui.user_promise.connect(self.create_intervention)
        
        button_giveUp: BasicButton = self.intervention_ui.buttons["choice_giveUp"]
        button_giveUp.clicked.connect()
        
    def create_intervention(self):
        self.IS.create_intervention
        