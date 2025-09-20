from ti.services.dataAccess.insightManager import InsightManager
from ti.services.engine.insightEngine import InsightEngine
from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import RawCardData, PresentedCardData
from ti.core.loggerService import LoggerService

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
        
        # 创建logger
        self.logger = LoggerService("./ti/features/insight", "conditional_generator")
        self.logger.log("初始化", f"条件报告生成器初始化完成，加载了 {len(recipe)} 个配方")
        
        # 连接信号
        self.IE._on_pattern_detected.connect(lambda d: self._on_pattern_detected(d))
        
    def create_report(self) -> list:
        """_summary_
        创建条件判断卡片的报告
        卡片会放进manager, 
        返回的时候，首先获取manager的卡片，作为返回值
        """  
        self.logger.log("报告生成", "开始生成条件卡片报告")
        
        # 在每次报告生成前, 重置Manager的状态
        self.IM.reset()
        
        cardData = []

        # 创建卡片
        for au in self.data:
            self.IE.process_action_unit(au)
        
        conditional_card = self.IM.get_current_cards()
        
        for card in conditional_card:
            card_type_id = card
            cardData.append(card)
            
        self.logger.log("报告完成", f"生成 {len(cardData)} 张条件卡片")
        return cardData
        

    
    def _on_pattern_detected(self,cardData: tuple[RawCardData, PresentedCardData]):
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
    