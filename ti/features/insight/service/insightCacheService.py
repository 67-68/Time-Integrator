
import uuid
from ti.features.insight.model.insight_card_generation_models import RawCardData, CacheCardData
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.features.yaml_database.service.yaml_parser_service import YamlParser


class InsightCacheService(IRepository):
    def __init__(self, yaml_parser: YamlParser):
        self.yaml_parser = yaml_parser
        self.allData = self._load_data()
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/model/data/insight_cache.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/model/data/insight_cache_rules.yaml"
    
    def _load_data(self):
        """
        从YAML文件加载缓存数据
        """
        try:
            # 检查规则文件是否为空
            rules_data = self.yaml.get_data(self.rule_file_path)
            
            if rules_data is None or rules_data == {}:
                # 规则文件为空，直接加载原始数据
                cache_data = self.yaml.get_data(self.filePath)
                cache_data = cache_data.get('insight_cache', {}) if cache_data else {}
            else:
                # 规则文件不为空，使用parse_data方法解析
                cache_data = self.yaml.parse_data(self.filePath, self.rule_file_path)
                cache_data = cache_data.get('insight_cache', {})
            
            return cache_data
            
        except Exception as e:
            print(f"Error loading insight cache data: {e}")
            return {}
    
    def save(self):
        """
        保存数据到YAML文件
        """
        try:
            data_to_save = {
                'insight_cache': self.allData
            }
            from ti.services.dataAccess import save_yaml_data
            save_yaml_data(data_to_save, self.filePath)
            return True
        except Exception as e:
            print(f"Error saving insight cache data: {e}")
            return False
    
    def load(self):
        """
        从YAML文件加载数据
        """
        self.allData = self._load_data()
        return self.allData
    
    def get_by_id(self, id: str):
        """
        通过id获取缓存数据
        """
        return self.allData.get(id, {})
    
    def get_all(self):
        """
        获取所有缓存数据
        """
        return self.allData
    
    def delete(self, id: str):
        """
        删除指定id的缓存数据
        """
        if id in self.allData:
            del self.allData[id]
            self.save()
            return True
        return False
    
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
            if id in self.allData:
                return self.allData[id]
        return self.allData
    
        
    
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
    
    def add_history_data(self,card: RawCardData) -> None:
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
        # 获取id
        id = card.id
        
        # 初始化
        data = {}
        
        # 创建CacheCardData对象
        cache_card = CacheCardData(
            card_id=str(uuid.uuid4()),
            id=card.id,
            weight=card.weight if card.weight is not None else 0.0,
            data=card.data
        )
        
        # 如果不存在
        if id not in self.allData:
            # 赋值data
            data = {
                "data":[],
                "total":{
                    "timeSpan":0,
                    "count":0
                }
            }   
            data["data"].append(cache_card.__dict__)
        else: # 如果存在
            # 首先检查是否卡片存在，需要修改
            for c in self.allData[id]["data"]:
                if c["card_id"] == cache_card.card_id:
                    c = cache_card.__dict__
                    break
            
            # 赋值data
            data = self.allData[id]
        
        # 这里目前用的是一个手动提取，未来可能换成子类注入的函数 不限制data的结构
        
        # 我决定加个补丁...如果是列表那么分开搞，如果是字典也分开搞
        
        # 补丁1: 列表检测
        #breakpoint() 
        if isinstance(card.data,list):
            for au in card.data: 
                data["total"]["timeSpan"] += au.timeSpan
                data["total"]["count"] += 1
        # 补丁2: 字典检测
        elif isinstance(card.data,dict):
            for key in card.data:
                data["total"]["timeSpan"] += card.data[key]["timeSpan"]
                data["total"]["count"] += 1
        
        self.allData[id] = data
        self.save()    
        
    def add_bulk_history_data(self,cards: list[RawCardData]) -> None:
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