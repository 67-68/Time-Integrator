
from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.service.insight_coordinator import InsightCoordinator
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
    def __init__(self):
        self.coordinator = None
    
    def assign_coordinator(self, coordinator):
        self.coordinator = coordinator
    
    def format_card(self, data:InsightCardModel):
        # 处理InsightCardModel对象
        judgement_key = data.judgements_texts
        sementic_key = data.card_type_id
        theme_key = data.title_text
        data_payLoad = data.model_dump()

        # Use InsightCoordinator to get specific narrative data
        self.database = self.coordinator.get_specific_narrative(sementic_key, "sementic_key")
        
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
                # Get judgement data using InsightCoordinator
                judgement_narrative = self.coordinator.get_specific_narrative(sementic_key, "judgement_key")
                if judgement_narrative is not None:
                    jDataList = judgement_narrative.get(judgement, [])
                    if jDataList:
                        judgement_data.append(randomChoser(jDataList).format(**data_payLoad))
        
        # 如果没有judgement数据，使用卡片原有的judgements文本
        if not judgement_data and "judgements_texts" in data_payLoad:
            judgement_data = data_payLoad["judgements_texts"]
        
        #  --- 获取title ---
        # Get presentation data using InsightCoordinator
        presentation_data = self.coordinator.get_specific_narrative(sementic_key, "presentation")
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
        
        # 如果输入是InsightCardModel，返回完整的InsightCardModel数据
        if hasattr(data, 'card_type_id'):
            pack["insight_card_model"] = {
                "sementic_text": sementic_data,
                "judgements_texts": judgement_data,
                "title_text": title,
                "color": color,
                "icon_path": icon,
                "icon_color": color,
                "card_type_id": sementic_key,
                "card_uuid": data.card_uuid,
                "create_time": data.create_time,
                "duration": data.duration,
                "current_state": data.current_state,
                "data_uuids": data.data_uuids,
                "detector_recipe_id": data.detector_recipe_id,
            }
        
        return pack
    
    
    
