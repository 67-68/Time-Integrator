from dataclasses import dataclass
from PyQt6.QtCore import QObject
from ti.core.eventBus import EventBus
from ti.features.intervention.model.model import INV_View_Recipe, INVEvent
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.service.stateMachine import INV_StateService
from ti.features.intervention.view.interventionCard import InterventionCard
from ti.features.refactored_intervention.presenter.IIntervention_Presenter import IInterventionPresenter

class INVCardPresenter(IInterventionPresenter):
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
        基本流程:
        EventSource
        1. 初始化自己，连接卡片按钮输入
        2. 如果卡片被激活
        查看配方中发布什么事件
        然后发布对应的事件
        
        View
        3. 接受来自eventbus的状态更新事件
        比对
        如果状态不一样
        更新自己
        可能需要引入新的状态配方设计
        不再是str状态而是时间线进展的状态
        
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
        
        # 2. 连接到修正后的 card信号
        self.ui.button_clicked.connect(lambda event: self._on_process_user_action(event))
        print("干涉卡片信号连接成功")
    
    # event source部分
    def _on_user_clicked(self,event):
        """
        作为Event source而存在
        这个函数负责查表用户的输入并发出事件
        查询路径为：
        当前状态-这个action-下一个状态
        
        Args:
            event (_type_): _description_
        """
        pass
    
    # 展示部分
    def _on_process_user_action(
        self,
        event: INVEvent
    ):
        """
        从事件中找到对应的状态并更新自己的UI
        
        Args:
            event_id (str): 被点击按钮的唯一ID, e.g., "choice_accept"。 
        # 目前直接定义按钮的显示文字，所见即所得
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
            
            # 切换当前状态
            print(f"presenter of {self.view_id} change from {self.current_state_key} to {next_state_key}")
            self.current_state_key = next_state_key