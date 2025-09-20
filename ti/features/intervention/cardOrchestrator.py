import uuid
from ti.features.insight.view.insight_card import InsightCard
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
        container: INV_ServiceContainer, #用来传递那些它不直接使用的服务
        bus: EventBus
    ):
        """
        它负责管理所有干涉卡片的生命周期
        """
        self.presenters: dict[InterventionPresenter] = {}
        self.factory = factory
        self.formatter = formatter
        self.repos = repos
        self.container = container
        self.bus = bus
        
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
        recipe = self.repos.get_by_id(view_id) # TODO: 这里的问题，返回了仅仅一部分的配方
        
        # 2. 创建卡片
        intervetion_card = self.factory.create_card(recipe)
        
        # 创建uuid
        view_uuid = uuid.uuid4()
        
        # 3. 创建presenter
        stateService = self.container.getService("stateService")
        bus = self.container.getService("bus")
        formatter = self.container.getService("formatter")
        presenter = InterventionPresenter (
            intervetion_card,
            recipe,
            bus,
            stateService,
            formatter,
            view_uuid
        )
        
        # 4. 添加卡片
        insightCard_ui.addWidget_inBottomLayout(intervetion_card)
        self.presenters[view_id] = presenter
        
        # 5. 保存干预数据到洞察卡片缓存
        self._save_intervention_data_to_cache(insightCard_ui, view_id, presenter)
        
        # 6. 保存洞察卡片
        self.save_insight_card(insightCard_id)
    
    def update_insightCard_with_data(
        self,
        insightCard_ui: InsightCard,
        insightCard_id:str,
        view_id: str,
        view_data: dict
    ):
        """
        使用缓存数据更新洞察卡片
        
        Args:
            insightCard_ui: 洞察卡片UI
            insightCard_id: 洞察卡片ID
            view_id: 视图配方ID
            view_data: 缓存中的视图数据
        """
        # 1. 获取配方
        recipe = self.repos.get_by_id(view_id)
        
        # 2. 创建卡片
        intervetion_card = self.factory.create_card(recipe)
        
        # 创建uuid
        view_uuid = uuid.uuid4()
        
        # 3. 创建presenter
        stateService = self.container.getService("stateService")
        bus = self.container.getService("bus")
        formatter = self.container.getService("formatter")
        presenter = InterventionPresenter (
            intervetion_card,
            recipe,
            bus,
            stateService,
            formatter,
            view_uuid
        )
        
        # 4. 使用缓存数据初始化presenter状态
        if hasattr(presenter, 'initialize_with_cache_data'):
            presenter.initialize_with_cache_data(view_data)
        
        # 5. 添加卡片
        insightCard_ui.addWidget_inBottomLayout(intervetion_card)
        self.presenters[view_id] = presenter
        
        # 6. 保存干预数据到洞察卡片缓存（使用更新后的数据）
        self._save_intervention_data_to_cache(insightCard_ui, view_id, presenter)
    
    def create_dialog_view(self,view_id) -> InterventionCard:
        view_recipe = self.repos.get_by_id(view_id)
        view_card = self.factory.create_card(view_recipe)
        presenter: InterventionPresenter = self.presenters[view_id]
        presenter.control_dialog_ui(view_card)
        return view_card

    def end_dialog(self,view_id):
        presenter: InterventionPresenter = self.presenters[view_id]
        presenter.end_control_dialog()
    
    def activate_presenter_state(
        self,
        view_id,
        event
    ):
        """
        手动给presenter传送一个事件

        Args:
            event (_type_): _description_
        """
        view:InterventionPresenter = self.presenters[view_id]
        view.process_event(event)
    
    def save_insight_card(self, insight_card_uuid: str):
        """
        发布保存洞察卡片事件
        
        Args:
            insight_card_uuid: 要保存的洞察卡片UUID
        """
        from ti.features.insight.model.insight_event import SaveInsightCard
        
        # 创建保存事件
        save_event = SaveInsightCard(
            "save_insight_card",
            insight_card_uuid
        )
        
        # 获取事件总线并发布事件
        
        if self.bus:
            self.bus.publish_event(SaveInsightCard, save_event)
            print(f"已发布保存洞察卡片事件: {insight_card_uuid}")
        else:
            print("错误: 无法获取事件总线服务")
    
    def _save_intervention_data_to_cache(self, insightCard_ui, view_id, presenter):
        """
        保存干预数据到洞察卡片缓存
        
        Args:
            insightCard_ui: 洞察卡片UI
            view_id: 视图配方ID
            presenter: 干预presenter实例
        """
        try:
            # 获取presenter的当前状态数据
            if hasattr(presenter, 'get_current_state_data'):
                view_data = presenter.get_current_state_data()
                
                # 保存到洞察卡片缓存
                insightCard_ui.cache['intervention_view_data'] = view_data
                insightCard_ui.cache['view_recipe_id'] = view_id
                
                print(f"已保存干预数据到洞察卡片缓存: {view_id}")
            else:
                print(f"警告: presenter没有get_current_state_data方法")
                
        except Exception as e:
            print(f"保存干预数据到缓存时发生错误: {e}")