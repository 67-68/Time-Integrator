
from Data import narratives
from Data.themes import themes
import random

from ti.core.definitions import Intervention_Card_State
from ti.utils import smart_formatter

"""
接收presenter(小)处理完成的数据
负责从对应的数据库中查找数据,会获取并返回
text:{
    judgement(s)
    sementic
}

presentation:{
    title
    icon
    color
}
"""
class FormatService:
    def __init__(self):
        pass
    def format_card(self,data):
        judgement_key = data["judgement_key"]
        sementic_key = data["sementic_key"]
        theme_key = data["card_type"]
        data_payLoad = data["data"]
        
        dataBase = narratives.SPECIFIC_NARRATION[sementic_key]
        
        #  --- 获取sementic ---
        sDataList = dataBase["sementic_key"]
        sementic_data = self.randomChoser(sDataList["text"])
        sementic_data = smart_formatter(data_payLoad,sementic_data)

        #  --- 获取judgement ---
        judgement_data = []
        for judgement in judgement_key:
            jDataList = dataBase["judgement_key"][judgement]
            judgement_data.append(self.randomChoser(jDataList).format(**data_payLoad))
        
        #  --- 获取title ---
        tDataList = dataBase["presentation"][theme_key]["title"]
        title = self.randomChoser(tDataList)
        
        #  --- 获取icon和颜色 ---
        icon = themes["icon"][theme_key]
        color = themes["color"][theme_key]

        #  --- 打包 ---
        pack = {
            "text":{
                "sementic":sementic_data,
                "judgement":judgement_data
            },
            "presentation":{
                "title":title,
                "icon":icon,
                "color":color
            },
        }
        
        #  --- 获取Intervention ---
        if "intervention" in data and data["intervention"] is not None:
            intervention_dataBase = data["intervention"]
            intervention_data = self.interventionFormat(inter_data=intervention_dataBase)
            pack["intervention"] = intervention_data
            
        return pack

    def randomChoser(self,list):
        """
        这个函数接收一个list
        在里面随机挑选一个返回
        """
        if len(list) == 1:
            return list[0]
        
        return random.choice(list)
    
    def interventionFormat(
        self,
        inter_data = None, #这里要加个状态机？
        inter_data_dict = None
        ):
        """_summary_

        Args:
            inter_data (Intervention_Recipe): 应该包含ID, Detector和State
            inter_data_dict(dict): 同上，但是dict
            
        Returns:
            _type_: _description_
        """
        
        if inter_data != None:
            #应该包含ID还有state
            intervention_id = inter_data.intervention_id #这里的Presenter传递出问题了，没有传送Detector
            intervention_state = inter_data.state.value
        else:
            intervention_id = inter_data_dict["id"]
            intervention_state = inter_data_dict["state"]

        intervention_base = narratives.INTERVENTION_TEXT
                    
        intervention_data = intervention_base[intervention_id] #包含Presentation和Choice

        intervention_title_list = intervention_data["presentation"][intervention_state]["title"]
        intervention_title = self.randomChoser(intervention_title_list)
        
        choice = {}
        
        intervention_choices_data = intervention_data["choice"]
        for choice_id in intervention_choices_data:
            choice_text = self.randomChoser(intervention_choices_data[choice_id])
            choice[choice_id] = choice_text
        
        pack = {
            "title": intervention_title,
            "choice": choice,
            "id": intervention_id,
            "state":intervention_state
        }
        
        return pack
