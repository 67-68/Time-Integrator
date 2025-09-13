from ti.features.insight.presenter.insight_card_presenter import InsightCardPresenter
from ti.features.insight.service.card_generation_service import InsightCardGeneration
from ti.features.insight.view.insight_card import InsightCard
from ti.features.insight.view.insight_view import InsightView


class InsightPresenter:
    def __init__(self):
        self.view = InsightView()
        self.generation = InsightCardGeneration()
        self.current_cards: list[InsightCardPresenter]
    
    def update_today_view(self):
        self.current_cards = self.create_today_cards()
        for card in self.current_cards:    
            card_view = card.card
            self.view.add_card(card_view)
    
    def create_today_cards(self) -> list[InsightCardPresenter]:
        return self.generation.create_today_cards()
        