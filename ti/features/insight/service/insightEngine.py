from PyQt6.QtCore import QObject,pyqtSignal

from ti.features.detector.model.baseDetector import BaseDetector
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.model import Detector_Recipe_ID
from ti.features.insight.service.insightCacheService import InsightCacheService
from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import RawCardData, CardInfo


class InsightEngine(QObject):
    """
    它负责调用所有被注册的detector,
    并接收它们的信号,传送给insightManager
    最终从Insight manager那里获取需要输出的卡片
    传送给presenter
    """
    _on_pattern_detected = pyqtSignal(tuple)
    def __init__(
        self,
        ICS: InsightCacheService,
        factory: DetectorFactory,
        parent = None
    ):
        """_summary_
        这个类会接收所有配方,
        给每个id的卡片创建一个字典，包含所有信息
        以及把信号连接上函数
    
        Args:
            recipes (list): 所有配方的列表
        """
        super().__init__(parent = None)    
        
        # 创建状态
        self.ICS = ICS
        self.factory = factory
        self.cards: Dict[str, CardInfo] = {}
    
    def initialize(self,recipes:list,cache: SessionCache):
        """_summary_
        这是Recipe传递的最后一环
        Args:
            recipes (list): _description_
        """
        for recipe in recipes:
            detector_id_str = recipe["detector"] 
            card_type_id = detector_id_str
            
            # Convert string detector ID to enum
            try:
                detector_id_enum = Detector_Recipe_ID(detector_id_str)
                detector: BaseDetector = self.factory.create_detector(detector_id_enum, card_type_id)
            except ValueError:
                print(f"Warning: Unknown detector ID '{detector_id_str}', skipping")
                continue
                        
            #这里，这一行，如果detector通过了，卡片模式被识别出来，会首先执行这一条
            detector.pattern_detected.connect(lambda f : self.pattern_detected(f))

            self.cards[card_type_id] = CardInfo(
                detector=detector,
                id=card_type_id,
                presenter=recipe["presenter"]
            )
            
            cache.store(card_type_id,(self.cards[card_type_id],recipe))
            
    def process_action_unit(self,au: dict) -> None:
        """_summary_
        这个函数会接收行动单元
        并按照内置的detector处理它们
        在检测到状态之后,会把洞察包送往insight manager,
        然后从它那里再重新获取需要输出的卡片
        把它们送给presenter之后
        返回获取到的文本和卡片信息
        需要获取结果，使用get_cur_cards
        Args:
            au (dict):一个行动单元
        """
        for id in self.cards:
            detector: BaseDetector = self.cards[id].detector
            detector.process_action_unit(au)
        
    def pattern_detected(self,rawData: dict) -> None:
        """_summary_
        这个函数是卡片模式被检测出来之后首先执行的
        它会把卡片信息加入insight manager, 以供调用
        Args:
            data (dict): 卡片模式的数据
        """
        # 将字典转换为RawCardData对象
        raw_card_data = RawCardData(
            id=rawData["id"],
            data=rawData["data"],
            weight=rawData.get("weight")
        )
        
        # 获取卡片id
        id = raw_card_data.id
        presenter = self.cards[id].presenter
        
        # 使用presenter处理
        pre_data = presenter(raw_card_data)
        
        # 发送信号
        #breakpoint()
        self._on_pattern_detected.emit((raw_card_data,pre_data)) #这里曾经出过问题，把元组作为参数发送
    