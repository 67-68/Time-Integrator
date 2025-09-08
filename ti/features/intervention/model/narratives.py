from ti.features.intervention.model.model import INV_View_ID, INVEvent, INV_View_Recipe


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
        data = NARRATIONS[intervention_id].get(sementic_id,None)
        
        return data
    
NARRATIONS = {
    INV_View_ID.POST_EAT_WASTE.value:{
        "init":{
            "presentation":{
                "title":["在吃饭后不要浪费时间的请求"],
                "button":{
                    INVEvent.USER_ACCEPTED.value:"接受挑战",
                    INVEvent.USER_REJECTED.value:"放弃"
                }
            }
        },
        "create_intervention":{
            "presentation":{
                "title":[""],
                "button":{
                    INVEvent.USER_ACCEPTED.value:"接受挑战",
                }
            }
        },
        "intervene_user":{
            "presentation":{
                "title":["在吃饭后不要浪费时间的请求"],
                "button":{
                    INVEvent.USER_ACCEPTED.value:"接受挑战",
                    INVEvent.USER_REJECTED.value:"放弃"
                }
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