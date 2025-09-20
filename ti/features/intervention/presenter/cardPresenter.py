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
        formatter: INV_Formatter,
        view_uuid: str
    ):
        """
        管理Intervention的类
        它作为Intervention卡片的数据来源
        卡片的每个行动都作为事件传入
        """
        super().__init__() # 调用父类的构造函数
        self.ui = ui
        self.view_id = ui.id
        self.view_uuid = view_uuid
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
            
            if not presentation:
                print(f"this state ({next_state_key}) have no presentation")
                return
            
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
    
    def process_event(self,event):
        """
        手动输入一个event

        Args:
            event (_type_): _description_
        """
        self._on_process_user_action(event)
        
    def switch_to_state(self, target_state_key: str):
        """
        强制跳转状态机到一个指定状态
        跳过正常的事件处理流程，直接切换到目标状态
        
        Args:
            target_state_key (str): 要跳转到的目标状态key（配方中定义的普通状态）
        """
        # 1. 验证目标状态是否存在
        target_state = self.recipe.state.get(target_state_key)
        if not target_state:
            print(f"错误：在配方中找不到目标状态 '{target_state_key}'")
            return False
        
        print(f"强制状态跳转: 从 '{self.current_state_key}' 到 '{target_state_key}'")
        
        # 2. 获取目标状态的presentation
        presentation = self.format.format(
            self.view_id,
            target_state_key
        )
        
        if not presentation:
            print(f"错误：状态 '{target_state_key}' 没有对应的presentation")
            return False
        
        # 3. 更新UI显示
        self.ui.apply_presentation(presentation)
        
        # 4. 如果存在对话框UI，也更新对话框
        if self.dialog_ui:
            self.dialog_ui.apply_presentation(presentation)
        
        # 5. 不要发布状态创建事件
        # TODO: 经过查找，我发现广播状态诞生和特殊状态special state的逻辑耦合在了一起 
        # 我之后需要把它们的逻辑(发布事件)分开
        
        # 6. 更新当前状态
        previous_state = self.current_state_key
        self.current_state_key = target_state_key
        
        print(f"状态跳转完成: {previous_state} -> {target_state_key}")
        return True
    
    def initialize_with_cache_data(self, cache_data: dict):
        """
        使用缓存数据初始化presenter状态
        
        Args:
            cache_data: 包含状态和UI数据的缓存字典
        """
        # 从缓存数据中恢复状态
        if 'current_state' in cache_data:
            self.current_state_key = cache_data['current_state']
            
            # 应用对应状态的presentation
            presentation = self.format.format(
                self.view_id,
                self.current_state_key
            )
            
            if presentation:
                self.ui.apply_presentation(presentation)
                
                # 如果存在对话框UI，也更新对话框
                if self.dialog_ui:
                    self.dialog_ui.apply_presentation(presentation)
        
        # 恢复其他UI状态（如果有的话）
        if 'ui_state' in cache_data:
            # 这里可以根据具体的UI状态数据进行恢复
            # 例如：按钮状态、输入框内容等
            ui_state = cache_data['ui_state']
            if hasattr(self.ui, 'restore_state'):
                self.ui.restore_state(ui_state)
        
        print(f"Presenter使用缓存数据初始化完成，当前状态: {self.current_state_key}")
    
@dataclass
class INV_State_Publish:
    recipe: INV_View_Recipe
    current_state_key: str
    view: InterventionCard
    special_state: list[str] = None