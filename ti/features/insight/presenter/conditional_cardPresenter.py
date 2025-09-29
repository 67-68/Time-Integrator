from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.service.insightManager import InsightManager
from ti.features.insight.service.insightEngine import InsightEngine
from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import RawCardData
from ti.services.loggerService import LoggerService

class Conditional_ReportGenerator():
    """_summary_
    这个类管理conditionalCard的创建
    同时管理engine和manager的通信
    """
    def __init__(
        self,
        data: dict,
        recipe: dict,
        IE: InsightEngine,
        IM: InsightManager,
        cache: SessionCache
    ):
        self.IE = IE
        self.IM = IM
        self.data = data
        self.recipe = recipe
        self.IE.initialize(recipe,cache)
        
        # 连接信号
        self.IE._on_pattern_detected.connect(lambda d: self._on_pattern_detected(d))
        
    def create_report(self) -> dict:
        """_summary_
        创建条件判断卡片的报告
        卡片会放进manager, 
        返回的时候，首先获取manager的卡片，作为返回值
        """  
        # 在每次报告生成前, 重置Manager的状态
        self.IM.reset()
        
        cardData = []

        # 创建卡片
        for au in self.data:
            self.IE.process_action_unit(au)
        
        cards_dict = {}
        cards = self.IM.get_current_cards()
        for card in cards:
            cards_dict[card.card_uuid] = card
            
        return cards_dict
        
    
    def _on_pattern_detected(self,cardData: tuple[RawCardData, InsightCardModel]):
        """_summary_
        这个函数连接了engine检测到模式之后的信号
        会把engine的信号和数据转接到Manager那里
        Args:
            cardData (tuple): 一个元组的数据，包含需要展示和需要储存的数据
        """
        
        # 提取元组
        rawData, preData = cardData
        
        # 添加卡片
        self.IM.add_card(rawData,preData)
    