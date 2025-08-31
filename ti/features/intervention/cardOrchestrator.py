from ti.UI.views.analysis.trendCard import InsightCard
from ti.core.eventBus import EventBus
from ti.features.intervention.model.view_repository import INV_Card_Repository
from ti.features.intervention.presenter.cardPresenter import InterventionPresenter
from ti.features.intervention.service.cardFactory import INV_Card_Factory
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.serviceContainer import INV_ServiceContainer
from ti.features.intervention.view.interventionCard import InterventionCard


class INV_Card_Orchestrator:
    def __init__(
        self,
        factory: INV_Card_Factory,
        formatter: INV_Formatter,
        repos: INV_Card_Repository,
        container: INV_ServiceContainer #用来传递那些它不直接使用的服务
    ):
        """
        它负责管理所有干涉卡片的生命周期
        """
        self.presenters = {}
        self.factory = factory
        self.formatter = formatter
        self.repos = repos
        self.container = container
        
    def update_insightCard(
        self,
        insightCard_ui: InsightCard,
        insightCard_id:str,
        view_id: str
    ):
        """
        这个方法用来在洞察卡片创建的时候给它加上干涉卡片

        Args:
            insightCard (InsightCard): _description_
        """
        # 1. 获取配方
        recipe = self.repos.get_recipe_by_id(view_id)
        
        # 2. 创建卡片
        intervetion_card = self.factory.create_card(recipe)
        
        # 3. 创建presenter
        stateService = self.container.getService("stateService")
        bus = self.container.getService("bus")
        formatter = self.container.getService("formatter")
        presenter = InterventionPresenter (
            intervetion_card,
            recipe,
            bus,
            stateService,
            formatter
        )
        
        # 4. 添加卡片
        insightCard_ui.addWidget_inBottomLayout(intervetion_card)
        self.presenters[view_id] = presenter
    
    def create_dialog_view(self,view_id) -> InterventionCard:
        view_recipe = self.repos.get_recipe_by_id(view_id)
        view_card = self.factory.create_card(view_recipe)
        presenter: InterventionPresenter = self.presenters[view_id]
        presenter.control_dialog_ui(view_card)
        return view_card

    def end_dialog(self,view_id):
        presenter: InterventionPresenter = self.presenters[view_id]
        presenter.end_control_dialog()
    
        
        
        