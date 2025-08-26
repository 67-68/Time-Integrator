from ti.features.intervention.model.model import Intervention_ID, InterventionRecipe


class InterventionNarrator:
    def __init__(self):
        """_summary_
        辅助获取Narrative数据
        """
        pass
    
    def get_text_by_id(
        self,
        intervention_id: str,
        sementic_id: str
    ):
        """_summary_
        这个函数会返回id指向的Intervention类
        数据里面的sementic id 指向的数据

        Args:
            intervention_id (str): _description_
            sementic_id (str): _description_

        Returns:
            _type_: _description_
        """
        data = NARRATIONS[intervention_id][sementic_id]
        
        return data
    
NARRATIONS = {
    Intervention_ID.POST_EAT_WASTE.value:{
        "init":{
            "presentation":{
                "title":["在吃饭后不要浪费时间的请求"],
            },
            "choice": { #到时候这里可以搞第一轮第二轮
                "choice_giveUp":["放弃"],
                "choice_accept":["接受挑战"]
            }
        }
    }
}
# 目前对于Intervention, 是写多少选项生成多少。同时，卡片选项会添加到list中，id(choice_giveUp)作为key, 文本直接展示

"""
在被Formatter处理过之后，形成类似这样的数据结构
pack = {
    "intervention" {
        "title": aaa,
        "choice": [
            "choice_id":"choice_text"
        ]
    }
}
"""