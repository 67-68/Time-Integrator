from PyQt6.QtCore import QObject
from dataclasses import dataclass
from Data.narratives import INTERVENTION_TEXT
from ti.UI.presenters.formatter import FormatService
from ti.features.intervention.view.InterventionCard import InterventionCard
from ti.UI.widgets.other.BasicLabel import BasicLabel
from ti.core.definitions import Intervention_Card_State

class InterventionPresenter(QObject):
    def __init__(
        self,
        ui: InterventionCard,
        card_event: Intervention_Card_State,
        FS: FormatService
    ):
        """
        管理Intervention的类
        它作为Intervention卡片的数据来源
        卡片的每个行动都作为事件传入
        """
        self.ui = ui
        self.id = ui.id
        self.FS = FS
        
        # 处理第一个事件
        self.process_user_action(card_event)

    def process_user_action(
        self,
        state:Intervention_Card_State
    ):
        """
        删除两个按钮，在按钮的位置添加label
        """
        # 这里需要修改State
        pack = self.FS.interventionFormat(inter_data_dict= {
            "id": self.id,
            "state": state
        })
        
        title = pack["title"]
        choice = pack["choice"] #新的按钮按理来说是先存着，以后用
        
        self.ui.deleteButton(Intervention_Card_State.USER_ACCEPTED.value)
        self.ui.deleteButton(Intervention_Card_State.USER_REJECTED.value)
        
        label = BasicLabel(self.ui,title)
        self.ui.addWidget_inButtonPlace(label)
        
        
        
        
        
        
