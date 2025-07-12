CARD_SUCCESS = "card_success"
CARD_WARNING = "card_warning"
CARD_INSIGHT = "card_insight"
CARD_DAILY_INFO = "card_daily_info"

#这里用来存储所有卡片GUI相关的数据，使用卡片名称作为key
themes = {
    "icon":{
        CARD_SUCCESS:"assets/icons/true_icon.svg",
        CARD_WARNING:"assets/icons/warning_icon.svg",
        CARD_INSIGHT:"assets/icons/insight_icon.svg",
        CARD_DAILY_INFO: "assets/icons/daily_info_icon.svg"
    },
    "color":{
        CARD_SUCCESS:"#FFFFFF",
        CARD_WARNING:"#FFFFFF",
        CARD_INSIGHT:"#FFFFFF",
        CARD_DAILY_INFO:"#FFFFFF"
    }
}
