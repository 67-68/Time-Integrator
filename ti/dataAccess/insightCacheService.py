
import uuid
from ti.core.definitions import INSIGHT_CACHE
from ti.dataAccess.dataAccess import getData


class InsightCacheService:
    def __init__(self):
        self.data = getData(INSIGHT_CACHE)
    
    def get_history_data(self,id:str = None) -> dict:
        """_summary_
        这个函数用来作为API 供其他人获取历史数据
        如果输入卡片id 那么返回该id的数据 如果不输入 那么返回全部卡片数据
        Args:
            id (str, optional): 卡片的id

        Returns:
            dict: 卡片数据
        """
        if id: 
            if id in self.data:
                return self.data[id]
        return self.data
    
        
    
    def create_new_data(self) -> dict:
        """_summary_
        返回一个卡片数据包裹
        Returns:
            dict: 一个卡片数据包
        """
        return {
            "weight":0,
            "history":{},
            "id":"",
            "data":[],
            "card_id":str(uuid.uuid4())
        }
    
    def add_history_data(self,card:dict) -> None:
        """_summary_
        这个函数用来给历史数据中添加内容
        它只会存储
        - 卡片信息:
            卡片uid
            模式id
            严重性
        
        - au信息(使用字典)
            - 状态名称(我想这个应该每个卡片都有)
                au uid
                au date(鬼知道未来会不会涉及跨天检测)
        """
        id = card["id"]
        if id not in self.data:
            data = {
                "data":[],
                "total":{
                    "timeSpan":0,
                    "count":0
                }
            }   
            data["data"].append(card)
        else:
            for c in data["data"]:
                if c["card_id"] == card["card_id"]:
                    c = card
                    break
        
        # 这里目前用的是一个手动提取，未来可能换成子类注入的函数 不限制data的结构
        
        # 我决定加个补丁...如果是列表那么分开搞，如果是字典也分开搞
        
        # 补丁1: 列表检测
        if isinstance(card[data],list):
            for au in card["data"]: 
                data["total"]["timeSpan"] += au["timeSpan"]
                data["total"]["count"] += 1
        # 补丁2: 字典检测
        elif isinstance(card["data"],dict):
            for key in card["data"]:
                data["total"]["timeSpan"] += card[data][key]["timeSpan"]
                data["total"]["count"] += 1
        
        self.data[id] = data    
        
    def add_bulk_history_data(self,cards:list) -> None:
        """_summary_
        这个函数用来给历史数据添加大批量的内容
        会调用多次add history data来添加内容
        Args:
            cards (list): 卡片数据的列表
        """
        for card in cards:
            self.add_history_data(card)
            
            
#最终结构
{
    "id":{
        "data":[ #presenter负责呈现的部分
            {
                "card_id":"",
                "id":"",
                "weight":0,
                "actionUnits":{
                    'stateName':{
                        "uid":"",
                        "date":""
                    }
                }
            }
        ],
        "total":{
            "timeSpan":0,
            "cardCount":0
        }
    }
}