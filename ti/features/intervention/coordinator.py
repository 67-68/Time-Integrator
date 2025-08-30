from ti.UI.views.analysis.trendCard import InsightCard
from ti.features.intervention.cardOrchestrator import INV_Card_Orchestrator
from ti.features.intervention.intervention_contract_orchestrator import INV_Contract_Orchestrator
from ti.features.intervention.model.model import INV_Entity_Recipe
from ti.features.intervention.service.mapping import InterventionMapping
from ti.features.intervention.serviceContainer import INV_ServiceContainer
from ti.services.sessionCache import SessionCache


class InterventionCoordinator:
    def __init__(
        self,
        container: INV_ServiceContainer,
        card_orchestrator: INV_Card_Orchestrator,
        contract_orchestrator: INV_Contract_Orchestrator
    ):
        self.container = container
        self.active_entity: dict[INV_Entity_Recipe] = {}
        self.card_orc = card_orchestrator
        self.contract_orc = contract_orchestrator
    
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
        insight_recipe = cache.read(insight_card_id)
        detector = insight_recipe["detector"]
        
        mapping:InterventionMapping = self.container.getService("mapping")
        needIntervention = mapping.find_mapping(insight_card_id)
        
        if needIntervention:
            for entity_recipe in needIntervention:
                # 加入实体
                entity_recipe: INV_Entity_Recipe
                entity_id = entity_recipe.entity_recipe_id
                self.active_entity[entity_id] = entity_recipe
                
                # 命令view
                self.card_orc.update_insightCard( # 把id和ui传入，其他的他自己处理
                    insight_card_ui,
                    insight_card_id
                )
                
                # 命令contract
                self.contract_orc.
                
                # TODO: 我写到这里！！
                
                # 知道了id之后可以去查找找到ui和配方