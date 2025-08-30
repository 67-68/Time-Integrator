from ti.UI.views.analysis.trendCard import InsightCard


class INV_Card_Orchestrator:
    def __init__(self):
        """
        它负责管理所有干涉卡片的生命周期
        """
        self.cards = {}
        
    def update_insightCard(
        self,
        insightCard_ui: InsightCard,
        insightCard_id:str
    ):
        """
        这个方法用来在洞察卡片创建的时候给它加上干涉卡片

        Args:
            insightCard (InsightCard): _description_
        """
        
        # 我开始搞orchestrator了，写完了mapping和repository之后就要开始推进entity的创建了