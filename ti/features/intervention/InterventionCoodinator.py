"""_summary_
鉴于这个功能覆盖面很广
不仅仅是一个页面内的交互而是牵扯到不同的页面和生命周期
因此选择Coodinator(MVP/MVC以上的层级)来协调而非Controller(MVC)
"""

from ti.UI.views.analysis.trendCard import TrendCard
from ti.core.Interfaces.Extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus


class InterventionCoodinator(ExtensionInterface):
    def __init__(self):
        """_summary_
        这是Intervention插件的主类
        掌管不同生命周期下的Intervention应该做什么
        首先它会获取卡片，然后在后面卡片制造的时候把它塞进去
        插件应该是先于主体部分加载的
        """
        # 获取卡片 
        
    
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
    def _on_card_created(self,ui: TrendCard):
        """_summary_
        这个类会看洞察卡片的类别是否匹配
        然后往里面塞对应的制造好的干涉卡片
        使用它的方法
        Args:
            ui (TrendCard): 洞察卡片的UI
        """
        