from ti.core.eventBus import EventBus
from ti.features.intervention.presenter.I_Card_Presenter import ICardPresenter
from ti.features.intervention.model.stored.inv_view_state import INVViewRecipe, ViewState, StatePresentation
from ti.features.intervention.model.events.inv_view_event import INVViewEvent, INVViewStateEvent
from ti.features.intervention.model.events.special_events import INVSpecialEvent
from ti.features.intervention.model.events.intervention_trigger import InterventionTriggered


class INVCardPresenter(ICardPresenter):
    """
    INVCardPresenter实现了ICardPresenter接口，负责卡片的状态管理和事件处理
    """
    
    def __init__(
        self,
        recipe: INVViewRecipe,
        bus: EventBus,
        project_id: str,
        _view_id: str
    ):
        ICardPresenter.__init__(self, parent=None)
        
        # 在Presenter内部创建View，减少耦合
        from ti.features.intervention.view.interventionCard import InterventionCard
        self._view = InterventionCard()
        
        self.recipe = recipe
        self.bus = bus
        self.project_id = project_id
        self._view_id = _view_id
        
        # 当前UI状态
        self.current_state = self.recipe.initial_state
        
        # 连接View的按钮点击事件
        self._view.button_clicked.connect(self._on_button_clicked)
        
        # 初始化UI
        self.apply_presentation()

    # --- 展示信息的函数 ---
    def apply_presentation(self):
        """
        这个方法用来把实际上获取的Presentation包展示出来
        它接受一个Presentation包
        """
        presentation = self.get_presentation()
        if presentation:
            self._view.apply_presentation(presentation)

    def get_presentation(self):
        """
        这个方法用来获取Presentation
        它接受一个状态，查找Presentation
        """
        if self.current_state not in self.recipe.state:
            return None
            
        current__view_state = self.recipe.state[self.current_state]
        return current__view_state.presentation

    def get_next_state(self, event: INVViewEvent):
        """
        这个方法用来获取下一个状态
        通过当前状态和一个INVViewEvent查找状态
        下一个状态被用来获取Presentation
        """
        if self.current_state not in self.recipe.state:
            return None
            
        current__view_state = self.recipe.state[self.current_state]
        return current__view_state.transition.get(event)
    
    # --- 用来发送事件的函数 ---
    def _on_button_clicked(self, event: INVViewEvent):
        """
        这个函数会接受一个从Button过来的INVViewEvent
        它会通过这个值获取下一个状态
        发送状态附加的事件: Special Events
        以及状态自己转换的事件之后: 
        (ViewState.entering_event)
        切换Presentation
        """
        next_state = self.get_next_state(event)
        
        if not next_state:
            print(f"Warning: No transition defined for event {event} in state {self.current_state}")
            return
        
        # 发送状态转换事件
        self.send_event(next_state)
        
        # 更新当前状态
        self.current_state = next_state
        
        # 应用新的Presentation
        self.apply_presentation()

    def send_event(self, next_state: str):
        """
        这个函数会接受一个状态，它负责发送这个状态所连带着的所有状态
        首先它会把Speicial_Event打包成为InterventionTriggered事件
        然后通过EventBus的Publish_Event方法发送
        """
        if next_state not in self.recipe.state:
            return
            
        next__view_state = self.recipe.state[next_state]
        
        # 发送状态转换事件
        state_event = INVViewStateEvent(
            previous_state=self.current_state,
            new_state=next_state,
            project_id=self.project_id,
            _view_id=self._view_id
        )
        self.bus.publish("intervention_state_changed", state_event)
        
        # 发送进入状态的特殊事件
        if next__view_state.entering_event:
            for event_name in next__view_state.entering_event:
                # 创建InterventionTriggered事件
                trigger_event = InterventionTriggered(
                    event_id=f"{self._view_id}_{next_state}_{event_name}",
                    inv_project_id=self.project_id,
                    special_event=event_name
                )
                self.bus.publish_event(InterventionTriggered, trigger_event)

    # BasePresenter abstract methods implementation
    def initialize(self):
        """初始化Presenter"""
        # Already initialized in __init__
        pass
    
    def shutdown(self):
        """关闭Presenter，清理资源"""
        # Disconnect signals and clean up
        if hasattr(self._view, 'button_clicked'):
            try:
                self._view.button_clicked.disconnect(self._on_button_clicked)
            except:
                pass
        
        self._view = None
        self.bus = None
        self.recipe = None
    
    def get_widget(self):
        """获取管理的Widget"""
        return self._view
    
    @property
    def name(self):
        return "intervention_card_presenter"
    
    @property
    def view(s):
        return s._view
    