from dataclasses import dataclass
from PyQt6.QtCore import QObject
from ti.core.eventBus import EventBus
from ti.features.intervention.model.model import INVRecipe, INVState
from ti.features.intervention.view.card import InterventionCard

class InterventionPresenter(QObject):
    def __init__(
        self,
        ui: InterventionCard,
        recipe: INVRecipe,
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

        # 1. 获取当前状态的完整对象
        current_state: INVState = self.recipe.state.get(self.current_state_key)
        
        
        event_id = event_id.value
    
        
        if not current_state:
            print(f"错误：在配方中找不到当前状态 '{self.current_state_key}'")
            return

        # 2. 从当前状态的转换规则(transition)中，查找此事件应该去往哪个新状态
        next_state_key = current_state.transition.get(event_id)
        
        if not next_state_key:
            print(f"警告：在状态 '{self.current_state_key}' 中没有为事件 '{event_id}' 定义转换规则。")
            # 在这里你可以决定是保持不动，还是进入一个错误/结束状态
            return
            
        # 3. 获取下一个状态的完整对象
        next_state: INVState = self.recipe.state.get(next_state_key)
        
        if not next_state:
            print(f"错误：在配方中找不到目标状态 '{next_state_key}'")
            return

        publish_pack = INV_State_Publish(
            self.recipe,
            self.current_state_key,
            self.ui
        )

        # 广播事件
        self.bus.publish(f"{next_state_key}_created",publish_pack)

        # 4. 更新Presenter的内部状态记录
        print(f"Transitioning from '{self.current_state_key}' to '{next_state_key}'")
        self.current_state_key = next_state_key
        
        # 5. 获取新状态的 "presentation" 配方
        presentation_to_apply = next_state.presentation
        
        # 6. 命令UI卡片应用新的 "presentation" 配方
        #    这会更新标题和按钮
        self.ui.apply_presentation(presentation_to_apply)

@dataclass
class INV_State_Publish:
    recipe: INVRecipe
    current_state_key: str
    ui: InterventionCard