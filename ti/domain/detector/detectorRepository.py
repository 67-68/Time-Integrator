from Data import userMatchers
from ti.core.analysis.matchers import Matcher
from ti.domain.detector.baseDetector import BaseDetector
from ti.domain.detector.modal import Detector_Config, Detector_Recipe, Detector_Recipe_ID, Detector_State


class DetectocRepository:
    def __init__(self):
        """_summary_
        这个类负责存储字典形式的配方并通过数据模型类把他们组装起来
        """
        pass
    
    def get_recipe_by_id(self,id:Detector_Recipe_ID) -> Detector_Recipe:
        """_summary_
        这个类接受一个Detector id
        根据id寻找配方组合为配方数据模型
        返回
        Args:
            id (Detector_Recipe_ID): _description_

        Returns:
            Detector_Recipe: _description_
        """
        recipe = RECIPE[id]
        sequences = recipe["config"]["sequence"]
        sequences_dataClass = [] #用来存储数据模型类
        
        # 创建状态数据模型
        for state in sequences:
            state_name = state["state_name"]
            matcher = state["matcher"]
            sequences_dataClass.append(Detector_State(state_name,matcher))
        
        # 按理来说中间应该还有一个Sequence数据模型,鉴于目前比较简单就省略了
        
        # 创建Config数据模型
        config_dataClass = Detector_Config(sequences_dataClass) 
        
        # 创建Recipe数据模型
        detector_type = recipe["detector"]
        recipe_dataClass = Detector_Recipe(detector_type,config_dataClass)

        return recipe_dataClass

matcher = Matcher()

RECIPE = {
    Detector_Recipe_ID.POST_EAT_WASTE.value: {
            "detector": BaseDetector,
            "config":{
                "sequence": [
                    {
                        "state_name": "meal",
                        "matcher": matcher.action_is("吃饭")
                    },
                    {
                        "state_name": "waste",
                        "matcher": matcher.action_type_is("waste")
                    }
                ],
            }
        }
}
