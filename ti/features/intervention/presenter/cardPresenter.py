from dataclasses import dataclass
from PyQt6.QtCore import QObject
from ti.core.eventBus import EventBus
from ti.features.intervention.model.model import INV_View_Recipe, INVState
from ti.features.intervention.view.card import InterventionCard

class InterventionPresenter(QObject):
    def __init__(
        self,
        ui: InterventionCard,
        recipe: INV_View_Recipe,
        bus: EventBus
    ):
        """
        管理Intervention的类
        它作为Intervention卡片的数据来源
        卡片的每个行动都作为事件传入
        """
        super().__init__() # 调用父类的构造函数
        self.ui = ui
        self.id = ui.id
        self.recipe = recipe
        self.bus = bus
        
        # 1. 增加一个属性来追踪当前状态，从配方的初始状态开始
        self.current_state_key = self.recipe.initial_state
        
        # 2. 连接到修正后的 card信号
        self.ui.button_clicked.connect(lambda event: self._on_process_user_action(event))
        print("干涉卡片信号连接成功")

    def _on_process_user_action(
        self,
        event_id: str
    ):
        """
        从用户点击事件的ID中找到对应的状态转换规则，并更新UI。
        这个函数同时负责更新UI
        在每次处理事件之后都更新UI, 防止Intervention临时卡片的请求被忽略
        
        Args:
            event_id (str): 被点击按钮的唯一ID, e.g., "choice_accept"。
        """
        print(f"Presenter for '{self.id}' received event: '{event_id}' from state '{self.current_state_key}'")

        publish_pack = INV_State_Publish(
            self.recipe,
            self.current_state_key,
            self.ui
        )
        
        # 广播事件
        self.bus.publish(f"{next_state_key}_created",publish_pack)
        
        # 6. 命令UI卡片应用新的 "presentation" 配方
        #    这会更新标题和按钮
        self.ui.apply_presentation(presentation_to_apply)

@dataclass
class INV_State_Publish:
    recipe: INV_View_Recipe
    current_state_key: str
    ui: InterventionCard