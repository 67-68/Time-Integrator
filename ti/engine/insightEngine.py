from PyQt6.QtCore import pyqtSignal,QObject
from ti.dataAccess.insightCacheService import InsightCache_service
from ti.dataAccess.insightManager import InsightManager

class InsightEngine(QObject):
    """
    它负责调用所有被注册的detector,
    并接收它们的信号,传送给insightManager
    最终从Insight manager那里获取需要输出的卡片
    传送给presenter
    """
    def __init__(self,recipes:list):
        """_summary_
        这个类会接收所有配方,
        给每个id的卡片创建一个字典，包含所有信息
        以及把信号连接上函数
    
        Args:
            recipes (list): 所有配方的列表
        """
        # 创建状态
        self.cards = {}
        self.ICS = InsightCache_service()
        self.IM = InsightManager(self.ICS)
        
        for recipe in recipes:
            id = recipe["id"]
            config = recipes
            
            detector = recipe["detector"](config,self.ICS)
            detector.pattern_detected.connect(lambda f : self.pattern_detected(f))
            
            self.cards[id] = {
                "detector": detector,
                "id":id
            }
            
        
    def __call__(self,au: dict) -> None:
        """_summary_
        这个函数会接收行动单元
        并按照内置的detector处理它们
        在检测到状态之后,会把洞察包送往insight manager,
        然后从它那里再重新获取需要输出的卡片
        把它们送给presenter之后
        返回获取到的文本和卡片信息
        
        Args:
            au (dict):一个行动单元
        """
        for id in self.cards:
            self.cards[id]["detector"](au)
        
    def pattern_detected(self,data: dict) -> None:
        self.IM.add_card(data)
    