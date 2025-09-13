from ti.features.insight.view.insight_card import InsightCard


class InsightCardPresenter:
    def __init__(
        self,
        card: InsightCard
    ):
        """
        卡片的presenter
        管理它

        Args:
            card (InsightCard): _description_
        """
        self.card = card
        
    @property
    def view(self):
        return self.card