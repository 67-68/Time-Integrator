from PyQt6.QtCore import QObject
from ti.dataAccess.insightCacheService import InsightCache_service
from ti.dataAccess.insightManager import InsightManager

class InsightEngine(QObject):
    """
    它负责调用所有被注册的detector,
    并接收它们的信号,传送给insightManager
    最终从Insight manager那里获取需要输出的卡片
    传送给presenter
    """        
    def __init__(self,recipes:list,parent = None):
        """_summary_
        这个类会接收所有配方,
        给每个id的卡片创建一个字典，包含所有信息
        以及把信号连接上函数
    
        Args:
            recipes (list): 所有配方的列表
        """
        super().__init__(parent)    
        
        # 创建状态
        self.cards = {}
        self.ICS = InsightCache_service()
        self.IM = InsightManager(self.ICS)
        
        for recipe in recipes:
            id = recipe["config"]["id"]
            config = recipe["config"]
            
            detector = recipe["detector"](config,self.ICS)
            
            #这里，这一行，如果detector通过了，卡片模式被识别出来，会首先执行这一条
            detector.pattern_detected.connect(lambda f : self.pattern_detected(f))
        
            self.cards[id] = {
                "detector": detector,
                "id":id,
                "presenter":recipe["presenter"]
            }
            
        
    def __call__(self,au: dict) -> None:
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
            self.cards[id]["detector"](au)
        
    def pattern_detected(self,data: dict) -> None:
        """_summary_
        这个函数是卡片模式被检测出来之后首先执行的
        它会把卡片信息加入insight manager, 以供调用
        Args:
            data (dict): 卡片模式的数据
        """
        self.IM.add_card(data)

        
    def get_cur_cards(self):
        """_summary_
        这个函数会首先通过insight manager获取当前的卡片数据, 把它们
        """
        return self.IM.get_current_cards()
    