from enum import Enum
from ti.features.detector import userMatchers
from ti.features.detector.matchers import Matcher
from ti.features.detector.baseDetector import BaseDetector
from ti.features.detector.model import Detector_Config, Detector_Recipe, Detector_Recipe_ID, Detector_Sequence, Detector_State


class DetectocRepository:
    def __init__(self):
        """_summary_
        这个类负责存储字典形式的配方并通过数据模型类把他们组装起来
        """
        pass
    
    def get_recipe_by_id(self,detector_id:Detector_Recipe_ID) -> Detector_Recipe:
        """_summary_
        这个类接受一个Detector id
        根据id寻找配方组合为配方数据模型
        返回
        Args:
            id (Detector_Recipe_ID): _description_

        Returns:
            Detector_Recipe: _description_
        """
        if isinstance(detector_id,Detector_Recipe_ID):
            recipe = RECIPE[detector_id.value]
        else:
            recipe = RECIPE[detector_id]
            
        sequences = recipe["config"]["sequence"]
    
        # HOOK部分
        hook_recipe = sequences["hook"]
        hook_dataClass = []
        result_recipe = sequences["result"]
        result_dataClass = []
        
        # 创建状态数据模型
        for state in hook_recipe:
            state_name = state["state_name"]
            matcher = state["matcher"]
            hook_dataClass.append(Detector_State(state_name,matcher))
            
        for state in result_recipe:
            state_name = state["state_name"]
            matcher = state["matcher"]
            result_dataClass.append(Detector_State(state_name,matcher))
        
        sequence_dataClass = Detector_Sequence(
            hook_dataClass,
            result_dataClass
        )
        
        # 创建Config数据模型
        config_dataClass = Detector_Config(sequence_dataClass) 
        
        # 创建Recipe数据模型
        detector_type = recipe["detector"]
        recipe_dataClass = Detector_Recipe(detector_type,config_dataClass)

        return recipe_dataClass

matcher = Matcher()


more_than_10_minute_waste = matcher.matchAll(
    matcher.action_type_is("waste"),
    matcher.duration_is_greater_than(10)
)





RECIPE = {
    Detector_Recipe_ID.POST_EAT_WASTE.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "meal",
                        "matcher": matcher.action_is("吃饭")
                    },
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": matcher.action_type_is("waste")
                    }
                ]
            }
        }
    },
    Detector_Recipe_ID.UNSETTLING_HEART.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "trivious_thing_1",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                    {
                        "state_name": "trivious_thing_2",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                    {
                        "state_name": "trivious_thing_3",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": more_than_10_minute_waste
                    }
                ]
            }
        }
    },
    Detector_Recipe_ID.POST_BASH_WASTE.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "bash",
                        "matcher": matcher.action_is("洗澡")
                    }
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": matcher.action_type_is("waste")
                    }
                ]
            }
        }
    },
}


