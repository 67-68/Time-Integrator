
from ti.features.insight.model.narratives import InsightNarrator
from ti.model.action_unit import ActionUnit
from ti.model.themes import themes
from ti.services.utils import randomChoser, smart_formatter

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
    def __init__(self, narrator: InsightNarrator):
        self.narrator = narrator
        
    def format_card(self,data):
        judgement_key = data["judgement_key"]
        sementic_key = data["sementic_key"]
        theme_key = data["card_type"]
        data_payLoad = data["data"]
        
        # Use InsightNarrator to get specific narrative data
        self.database = self.narrator.get_specific_narrative(sementic_key, "sementic_key")
        
        #  --- 获取sementic ---
        sDataList = self.database
        sementic_data = randomChoser(sDataList["text"])
        sementic_data = smart_formatter(data_payLoad,sementic_data)

        #  --- 获取judgement ---
        judgement_data = []
        for judgement in judgement_key:
            # Get judgement data using InsightNarrator
            jDataList = self.narrator.get_specific_narrative(sementic_key, "judgement_key").get(judgement, [])
            judgement_data.append(randomChoser(jDataList).format(**data_payLoad))
        
        #  --- 获取title ---
        # Get presentation data using InsightNarrator
        presentation_data = self.narrator.get_specific_narrative(sementic_key, "presentation")
        tDataList = presentation_data.get(theme_key, {}).get("title", [])
        title = randomChoser(tDataList)
        
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
            "id":sementic_key
        }
        
        return pack
