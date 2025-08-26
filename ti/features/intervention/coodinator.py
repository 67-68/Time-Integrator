"""_summary_
鉴于这个功能覆盖面很广
不仅仅是一个页面内的交互而是牵扯到不同的页面和生命周期
因此选择Coodinator(MVP/MVC以上的层级)来协调而非Controller(MVC)
"""

from ti.UI.views.analysis.trendCard import TrendCard
from ti.core.Interfaces.Extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.intervention.cardFactory import InterventionCard_Factory
from ti.features.intervention.formatter import InterventionFormatter
from ti.features.intervention.model.model import InterventionFactory_Pack
from ti.features.intervention.model.narratives import InterventionNarrator
from ti.features.intervention.model.repository import InterventionRepository
from ti.features.intervention.presenter.cardPresenter import InterventionPresenter
from ti.services.sessionCache import SessionCache


class InterventionCoodinator(ExtensionInterface):
    def __init__(self):
        """_summary_
        这是Intervention插件的主类
        掌管不同生命周期下的Intervention应该做什么
        首先它会获取卡片，然后在后面卡片制造的时候把它塞进去
        插件应该是先于主体部分加载的
        """
        
        # 创建服务
        self.repository = InterventionRepository()
        self.narrator = InterventionNarrator()
        self.formatter = InterventionFormatter(self.narrator)
        self.factory = InterventionCard_Factory(self.repository,self.formatter)
        
        
        # 创建配方中的卡片；主要的数据交给Coodinator管理
        self.cards: list[InterventionFactory_Pack] = self.factory.create_cards()
    
    # ------ 接口方法 ——----    
    
    @property
    def name(self):
        return "Intervention"
    
    def initialize(self, eventBus:EventBus):
        """_summary_
        目前暂定接受UI卡片完成的信号
        直接塞进UI
        在未来可能会考虑设计UI积木语法
        Args:
            eventBus (_type_): _description_
        """
        eventBus.subscribe("insight_card_ui_created",self._on_card_created)
    
    def shutdown(self):
        return super().shutdown()
    
    # ------ 业务逻辑 ——----
    def _on_card_created(self,data: tuple):
        """_summary_
        这个类会看洞察卡片的类别是否匹配
        然后往里面塞对应的制造好的干涉卡片
        使用它的方法
        它仅仅只是塞进UI
        并没有激活Monitor监视器
        Args:
            ui (TrendCard): 洞察卡片的UI
        """
        card_ui,cache = data
        cache: SessionCache
        card_ui: TrendCard
        
        card_id = card_ui.id
        
        cardRecipe = cache.read(card_id)
            
        for intervention_id in self.cards:
            if card_id == intervention_id:
                # 获取Detecotor, 存入配方
                recipe = self.cards[intervention_id].recipe
                
                if recipe.detector == None:
                    detector = cardRecipe["detector"]
                    recipe.detector = detector
                    #目前我的Intervention和卡片配方必须1:1对应啊...要不然加一个对应卡片配方key?
                
                # 创建卡片
                intervention_ui = self.cards[intervention_id].ui
                card_ui.addWidget_inBottomLayout(intervention_ui)
                
                # 创建Presenter
                presenter = InterventionPresenter(intervention_ui,self.formatter,recipe)

        
        # 另一个问题：Intervention如何接触数据？ 塞进SessionCache吧
        