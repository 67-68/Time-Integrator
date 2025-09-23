
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
class InsightFormatService:
    def __init__(self, narrator: InsightNarrator):
        self.narrator = narrator
    
    def assign_narrator(self,narrator):
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
        if sDataList is None:
            # 如果找不到narrative数据，使用卡片原有的sementic文本
            sementic_data = data_payLoad.get("sementic_text", "No narrative data available")
        else:
            sementic_data = randomChoser(sDataList["text"])
            sementic_data = smart_formatter(data_payLoad,sementic_data)

        #  --- 获取judgement ---
        judgement_data = []
        if judgement_key:  # 只有judgement_key不为空时才处理
            for judgement in judgement_key:
                # Get judgement data using InsightNarrator
                judgement_narrative = self.narrator.get_specific_narrative(sementic_key, "judgement_key")
                if judgement_narrative is not None:
                    jDataList = judgement_narrative.get(judgement, [])
                    if jDataList:
                        judgement_data.append(randomChoser(jDataList).format(**data_payLoad))
        
        # 如果没有judgement数据，使用卡片原有的judgements文本
        if not judgement_data and "judgements_texts" in data_payLoad:
            judgement_data = data_payLoad["judgements_texts"]
        
        #  --- 获取title ---
        # Get presentation data using InsightNarrator
        presentation_data = self.narrator.get_specific_narrative(sementic_key, "presentation")
        if presentation_data is not None:
            tDataList = presentation_data.get(theme_key, {}).get("title", [])
            title = randomChoser(tDataList) if tDataList else ""
        else:
            # 如果找不到presentation数据，使用卡片原有的title文本
            title = data_payLoad.get("title", "")
        
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
