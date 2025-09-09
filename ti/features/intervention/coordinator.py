from ti.features.insight.model.insight_card_generation_models import FixedCardResult
from ti.features.insight.view.trendCard import InsightCard
from ti.core.eventBus import EventBus
from ti.features.intervention.cardOrchestrator import INV_Card_Orchestrator
from ti.features.intervention.intervention_contract_orchestrator import INV_Contract_Orchestrator
from ti.features.intervention.model.model import INV_Entity_Recipe, INVEvent
from ti.features.intervention.service.mapping import InterventionMapping
from ti.features.intervention.serviceContainer import INV_ServiceContainer
from ti.services.sessionCache import SessionCache


class InterventionCoordinator:
    def __init__(
        self,
        container: INV_ServiceContainer,
        card_orchestrator: INV_Card_Orchestrator,
        contract_orchestrator: INV_Contract_Orchestrator,
        bus: EventBus
    ):
        self.container = container
        self.active_entity: dict[INV_Entity_Recipe] = {}
        self.card_orc = card_orchestrator
        self.contract_orc = contract_orchestrator
        self.bus = bus
        
        self.contract_orc.contract_activated.connect(lambda d: self._on_contract_activated(d))
        
        
    
    def process_insight_card(self,data: tuple):
        """_summary_
        这个类会看洞察卡片的类别是否匹配
        然后往里面塞对应的制造好的干涉卡片
        使用它的方法
        它仅仅只是塞进UI
        并没有激活Monitor监视器
        Args:
            ui (TrendCard): 洞察卡片的UI
        """
        insight_card_ui,cache = data
        cache: SessionCache
        insight_card_ui: InsightCard
        insight_card_id = insight_card_ui.id
        pack = cache.read(insight_card_id) #存入的地方在InsightEngine
        if isinstance(pack,tuple): #只有conditional card才有一个tuple
            insight_recipe, recipe = pack
        else: 
            recipe = pack
        if not isinstance(recipe,FixedCardResult):
            detector_recipe_key = recipe.get("detector",None) #不是COnditioanl card没有detector
        
        mapping:InterventionMapping = self.container.getService("mapping")
        needIntervention = mapping.find_mapping(insight_card_id)
        
        if needIntervention:
            for entity_recipe in needIntervention:
                # 加入实体
                entity_recipe: INV_Entity_Recipe
                entity_id = entity_recipe.entity_recipe_id
                self.active_entity[entity_id] = entity_recipe
                contract_id = entity_recipe.contract_recipe
                view_id = entity_recipe.view_recipe_id
                
                # 命令view
                self.card_orc.update_insightCard( # 把id和ui传入，其他的他自己处理
                    insight_card_ui,
                    insight_card_id,
                    view_id
                )
                
                # 命令contract
                self.contract_orc.create_contract(
                    contract_id,
                    detector_recipe_key
                )
                
    def _on_contract_activated(self,view_id):
        # 应该使用一个eventbus的事件，从contract orc -> card orc推进 
        # 但是先不管他
        # 推进状态
        event = INVEvent.INTERVENTION_CREATED # 这里不需要.value因为它本来就是处理一个类
        self.card_orc.activate_presenter_state(view_id,event)
        
        # 获取ui
        card = self.card_orc.create_dialog_view(view_id)
        
        # 上报app类
        self.bus.publish("dialog_needed",card) 
        # 按理来说这里是需要一个Enum事件，可以在事件的同时发布id，一个开始id接一个结束id 
        # 或者其实在app端这么搞也行不用事件，不直接写出来而是app自己接收事件查找关闭
        
        
        # 删除card 按理来说上报之后应该会有一个dialog阻塞住事件?
        self.card_orc.end_dialog(view_id)