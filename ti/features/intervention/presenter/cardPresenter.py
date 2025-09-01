from dataclasses import dataclass
from PyQt6.QtCore import QObject
from ti.core.eventBus import EventBus
from ti.features.intervention.model.model import INV_View_Recipe, INVEvent
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.service.stateMachine import INV_StateService
from ti.features.intervention.view.interventionCard import InterventionCard

class InterventionPresenter(QObject):
    def __init__(
        self,
        ui: InterventionCard,
        recipe: INV_View_Recipe,
        bus: EventBus,
        stateService: INV_StateService,
        formatter: INV_Formatter
    ):
        """
        管理Intervention的类
        它作为Intervention卡片的数据来源
        卡片的每个行动都作为事件传入
        """
        super().__init__() # 调用父类的构造函数
        self.ui = ui
        self.view_id = ui.id
        self.recipe = recipe
        self.bus = bus
        self.stateService = stateService
        self.format = formatter
        self.dialog_ui = None
        
        # 1. 增加一个属性来追踪当前状态，从配方的初始状态开始
        self.current_state_key = self.recipe.initial_state
        
        # 2. 连接到修正后的 card信号
        self.ui.button_clicked.connect(lambda event: self._on_process_user_action(event))
        print("干涉卡片信号连接成功")
        
        
        # 发布第一个event
        current_state = self.recipe.state[self.current_state_key]
        special_event = current_state.special_event
        publish_pack = INV_State_Publish(
            self.recipe,
            self.current_state_key,
            self.ui,
            special_event
        )
        self.bus.publish(f"{self.current_state_key}_created",publish_pack)

    def _on_process_user_action(
        self,
        event: INVEvent
    ):
        """
        从用户点击事件的ID中找到对应的状态转换规则，并更新UI。
        这个函数同时负责更新UI
        在每次处理事件之后都更新UI, 防止Intervention临时卡片的请求被忽略
        
        Args:
            event_id (str): 被点击按钮的唯一ID, e.g., "choice_accept"。
        """
        event_id = event.value
        print(f"Presenter for '{self.view_id}' received event: '{event_id}' from state '{self.current_state_key}'")
        
        next_state = self.stateService.process_event(
            event_id,
            self.current_state_key,
            self.recipe
        )
        
        if not next_state:
            print(f"没有定义{self.current_state_key}在{event_id}下的转换规则")
            return
        
        next_state_key = next_state.name
        special_event = next_state.special_event
        
        if next_state_key:
            publish_pack = INV_State_Publish(
                self.recipe,
                self.current_state_key,
                self.ui,
                special_event
            )
            
            # 广播事件
            self.bus.publish(f"intervention_state_created",publish_pack)
            
            # 获取配方对应的presentation
            presentation = self.format.format(
                self.view_id,
                next_state_key
            )
            
            self.ui.apply_presentation(presentation)
            
            # 判断是否extraUi也要切换; 我觉得这是一个不好的设计，但大概可以用;
            # 或许需要把state获取和这一大堆的警示文本解耦出来成为一个Function
            if self.dialog_ui:
                self.dialog_ui.apply_presentation(presentation)
            
            # 切换当前状态
            print(f"presenter of {self.view_id} change from {self.current_state_key} to {next_state_key}")
            self.current_state_key = next_state_key

    def control_dialog_ui(
        self,
        card: InterventionCard
    ):
        self.dialog_ui = card
        self.dialog_ui.button_clicked.connect(self._on_process_user_action)
    
    def end_control_dialog(self):
        self.dialog_ui = None
        # 或许要把信号连接也斩断？
        # 特殊事件来自毁？
    
@dataclass
class INV_State_Publish:
    recipe: INV_View_Recipe
    current_state_key: str
    view: InterventionCard
    special_state: list[str] = None