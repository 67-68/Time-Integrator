from PyQt6.QtCore import QObject
from ti.features.capture.view.capture import CaptureView
from ti.features.capture_test.model.protocols.capture_renderable_item import RenderableItemModel
from ti.features.capture_test.model.selection_condition import SelectionCondition
from ti.features.capture_test.presenter.context_selection_presenter import ContextSelectionPresenter
from ti.features.capture_test.presenter.item_display_presenter_interface import IItemDisplayPresenter
from ti.features.capture_test.presenter.item_editor_presenter_interface import IItemEditorPresenter
from ti.presenters.BasePresenter import BasePresenter
from ti.services.dataService import DataService
from ti.core.eventBus import EventBus
from ti.services.group_manager import PresenterGroupManager

class CapturePresenter(BasePresenter):
    """
    CapturePresenter 管理 Capture 插件的核心业务逻辑，
    协调不同的功能组件。
    """
    
    def __init__(
        self,
        data_service: DataService,
        event_bus: EventBus,
        context_selection_presenters: list[ContextSelectionPresenter],
        item_display_presenters: list[IItemDisplayPresenter],
        item_editor_presenters: list[IItemEditorPresenter],
        data_models: list[RenderableItemModel]
    ):
        super().__init__()
        self.data_service = data_service
        self.event_bus = event_bus

        # 1. 使用 Manager 替换重复的字典和 active 状态
        self.context_selectors = PresenterGroupManager(context_selection_presenters)
        self.item_displays = PresenterGroupManager(item_display_presenters)
        self.item_editors = PresenterGroupManager(item_editor_presenters)

        self.models = {model.data_model: model for model in data_models}
        
        # 2. 将初始化和设置逻辑分解成更小、更清晰的方法
        self._initialize_presenters()
        
        self._view = CaptureView()
        self._setup_view()
        self._connect_signals()

        self.refresh_and_distribute_display_data()

    def _initialize_presenters(self) -> None:
        """初始化所有子 Presenter"""
        self.context_selectors.initialize_all()
        self.item_displays.initialize_all()
        self.item_editors.initialize_all()
        
    def _setup_view(self) -> None:
        """设置视图布局，将 Presenter 的视图添加到 Tab 中"""
        # 3. 循环变得更简洁
        for name, presenter in self.context_selectors.presenters.items():
            self._view.add_tab(self._view.TabType.CONTEXT_SELECTION, presenter.view, name)

        for name, presenter in self.item_displays.presenters.items():
            self._view.add_tab(self._view.TabType.ITEM_DISPLAY, presenter.view, name)

        for name, presenter in self.item_editors.presenters.items():
            self._view.add_tab(self._view.TabType.ITEM_EDITOR, presenter.view, name)
    
    def _connect_signals(self) -> None:
        """连接所有子 Presenter 和 View 的信号"""
        # 4. 信号连接更清晰
        self.context_selectors.connect_all(self._on_selection_condition_changed)
        self.item_displays.connect_all(self._on_item_selected)
        
        # 连接 View 的 Tab 变化信号
        self._view.tab_changed.connect(self._on_tab_changed)

    def _on_tab_changed(self, tab_type, tab_name: str) -> None:
        """统一处理所有 Tab 切换事件"""
        # 5. 一个方法处理所有 Tab 切换，而不是三个
        if tab_type == self._view.TabType.CONTEXT_SELECTION:
            self.context_selectors.active = self.context_selectors.get(tab_name)
            print(f"激活的 Context Selection Presenter: {tab_name}")
        elif tab_type == self._view.TabType.ITEM_DISPLAY:
            self.item_displays.active = self.item_displays.get(tab_name)
            print(f"激活的 Item Display Presenter: {tab_name}")
        elif tab_type == self._view.TabType.ITEM_EDITOR:
            self.item_editors.active = self.item_editors.get(tab_name)
            print(f"激活的 Item Editor Presenter: {tab_name}")
    
    def refresh_and_distribute_display_data(self, selection_condition: SelectionCondition = None):
        """根据选择条件，刷新并分发数据到所有 Item Display Presenters"""
        if not selection_condition and self.context_selectors.active:
            selection_condition = self.context_selectors.active.get_selection_condition()
        
        # 6. 这里的逻辑可以进一步优化，但目前保持原样以专注于结构
        for model in self.models.values():
            model_data = self.data_service.parse_selection_condition(selection_condition)
            for display_name in model.item_displayable_list:
                # 使用 manager 获取 presenter
                display_presenter = self.item_displays.get(display_name)
                if display_presenter:
                    display_presenter.add_data(model_data)

    def _refresh_item_editor_presenter(self, data_model):
        """刷新 Item Editor Presenter 以显示选中项的数据"""
        print(f"Refreshing item editor presenter with data: {data_model}")
        
        model_type = type(data_model)
        if model_type not in self.models:
            return

        editorable_list = self.models[model_type].item_editorable_list
        
        # 7. 优先使用当前激活的 editor
        active_editor = self.item_editors.active
        # 潜在bug修复：比较 presenter 的 name 而不是实例
        if active_editor and active_editor.name in editorable_list:
            active_editor.fill_data(data_model)
            return
        
        # 如果当前激活的不合适，则查找第一个合适的并切换过去
        for editor_name in editorable_list:
            editor = self.item_editors.get(editor_name)
            if editor:
                editor.fill_data(data_model)
                self._view.switch_to_tab(editor.name)
                return

    def _on_selection_condition_changed(self, selection_condition):
        """处理选择条件变化事件"""
        print(f"Capture presenter received selection condition: {selection_condition}")
        # 填充记录列表
        self.refresh_and_distribute_display_data(selection_condition=selection_condition)
        
    def _on_save_requested(self, action_unit):
        """
        处理保存请求
        :param property_data: 属性数据字典
        """ 
        # 保存到数据服务
        self.data_service.add_actionUnit(action_unit)
        
        # 刷新各个widget
        self._refresh_all_widgets()
        
        # 重置删除计数器
        self.input.button_group.reset_delete_count()
    
    def _on_item_selected(self, data):
        """
        处理记录项选择事件
        """
        print(f"Capture presenter received data: {data}")
        self._refresh_item_editor_presenter(data)
    
    def _refresh_item_editor_presenter(self, data_model):
        """刷新item editor presenter"""
        print(f"Refreshing item editor presenter with action unit: {data_model}")
        
        # 查找合适的Editor, 目前找到第一个就填充
        editorable_list = self.models[type(data_model)].item_editorable_list
        if self.active_item_editor_presenter in editorable_list:
            self.active_item_editor_presenter.fill_data(data_model)
            return
        
        for view in self.item_editor_presenters.values():
            if view in editorable_list:
                view.fill_data(data_model)
                self.switch_to_tab(view.name)

    def switch_to_tab(self, presenter_name):
        """切换到指定名称的presenter tab"""
        return self._view.switch_to_tab(presenter_name)
                
    def initialize(self):
        return super().initialize()
    
    def shutdown(self):
        return super().shutdown()
    
    @property
    def name(self):
        return "capture_presenter"
    
    @property
    def view(s):
        return s._view