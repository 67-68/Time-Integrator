from Data import narratives
from Data.themes import themes
import random

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

def format_card(data):
    judgement_key = data["judgement_key"]
    sementic_key = data["sementic_key"]
    theme_key = data["card_type"]
    au = data["data"]
    
    dataBase = narratives.SPECIFIC_NARRATION[sementic_key]
    #  --- 获取sementic ---
    sDataList = dataBase["sementic_key"]
    sementic_data = randomChoser(sDataList)
    sementic_data.format(**au)
    
    #  --- 获取judgement ---
    judgement_data = []
    for judgement in judgement_key:
        jDataList = dataBase["judgement_key"][judgement]
        judgement_data.append(randomChoser(jDataList))
    
    #  --- 获取title ---
    tDataList = dataBase["presentation"][theme_key]
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
        }
    }
    
    return pack

def randomChoser(list):
    """
    这个函数接收一个list
    在里面随机挑选一个返回
    """
    return list[random.randint(0,len(list)-1)]