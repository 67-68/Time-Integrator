
import uuid
from ti.core.definitions import INSIGHT_CACHE
from ti.dataAccess.dataAccess import getData


class InsightCache_service:
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
        这个函数用来给历史数据中添加内容，
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
        for au in card["data"]:
            data["total"]["timeSpan"] += au["timeSpan"]
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
        "data":[],
        "total":{
            "timeSpan":0,
            "cardCount":0
        }
    }
}