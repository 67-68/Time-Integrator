import logging
from ti.features.capture.view.capture_view import CaptureView
from ti.features.capture.model.protocols.capture_renderable_item import RenderableItemModel
from ti.features.capture.model.selection_condition import SelectionCondition
from ti.features.capture.presenter.context_selection_presenter import ContextSelectionPresenter
from ti.features.capture.presenter.item_display_presenter_interface import IItemDisplayPresenter
from ti.features.capture.presenter.item_editor_presenter_interface import IItemEditorPresenter
from ti.presenters.BasePresenter import BasePresenter
from ti.services.dataService import DataService
from ti.core.eventBus import EventBus


class CapturePresenter(BasePresenter):
    """
    CapturePresenter管理capture插件的业务逻辑
    协调UI组件和数据服务
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
        
        # 将presenter列表转换为字典，使用name作为key
        self.context_selection_presenters = {presenter.name: presenter for presenter in context_selection_presenters}
        self.item_display_presenters = {presenter.name: presenter for presenter in item_display_presenters}
        self.item_editor_presenters = {presenter.name: presenter for presenter in item_editor_presenters}

        # 跟踪激活的界面状态
        self.active_context_selection_presenter = None
        self.active_item_display_presenter = None
        self.active_item_editor_presenter = None

        # 初始化所有presenter
        for presenter in self.context_selection_presenters.values():
            presenter.initialize()
        for presenter in self.item_display_presenters.values():
            presenter.initialize()
        for presenter in self.item_editor_presenters.values():
            presenter.initialize()

        # 创建主视图并设置布局
        self._view = CaptureView()
        self._setup_view_layout()

        # 准备data model
        self.models = {model.base_model: model for model in data_models} # key = datamodel class
        self.refresh_and_distribute_display_data()
        
    def _setup_view_layout(self):
        """设置视图布局 - 使用三个TabWidget分别组织presenter视图"""
        # 添加context selection presenters到View的TabWidget
        for name, presenter in self.context_selection_presenters.items():
            self.view.add_context_selection_tab(presenter.view, name)

        # 添加item display presenters到View的TabWidget
        for name, presenter in self.item_display_presenters.items():
            self.view.add_item_display_tab(presenter.view, name)

        # 添加item editor presenters到View的TabWidget
        for name, presenter in self.item_editor_presenters.items():
            self.view.add_item_editor_tab(presenter.view, name)

        # 连接View的Tab变化信号
        self.view.context_selection_tab_changed.connect(self._on_context_selection_tab_changed)
        self.view.item_display_tab_changed.connect(self._on_item_display_tab_changed)
        self.view.item_editor_tab_changed.connect(self._on_item_editor_tab_changed)

        # 设置初始激活状态
        self._set_initial_active_state()

        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        """连接所有信号"""
        # 连接所有context selection presenters的信号
        for presenter in self.context_selection_presenters.values():
            presenter.selection_condition_changed.connect(self._on_selection_condition_changed)

        # 连接所有item display presenters的信号
        for presenter in self.item_display_presenters.values(): #
            presenter.item_selected.connect(self._on_item_selected)

    def _on_context_selection_tab_changed(self, tab_name):
        """处理Context Selection Tab变化事件"""
        self.active_context_selection_presenter = self.context_selection_presenters.get(tab_name)
        print(f"激活的Context Selection Presenter: {tab_name}")

    def _on_item_display_tab_changed(self, tab_name):
        """处理Item Display Tab变化事件"""
        self.active_item_display_presenter = self.item_display_presenters.get(tab_name)
        print(f"激活的Item Display Presenter: {tab_name}")

    def _on_item_editor_tab_changed(self, tab_name):
        """处理Item Editor Tab变化事件"""
        self.active_item_editor_presenter = self.item_editor_presenters.get(tab_name)
        print(f"激活的Item Editor Presenter: {tab_name}")

    def _set_initial_active_state(self):
        """设置初始激活状态"""
        # 设置Context Selection的初始激活状态
        if self.context_selection_presenters:
            first_context_name = next(iter(self.context_selection_presenters.keys()))
            self.active_context_selection_presenter = self.context_selection_presenters[first_context_name]
            print(f"初始激活的Context Selection Presenter: {first_context_name}")

        # 设置Item Display的初始激活状态
        if self.item_display_presenters:
            first_display_name = next(iter(self.item_display_presenters.keys()))
            self.active_item_display_presenter = self.item_display_presenters[first_display_name]
            print(f"初始激活的Item Display Presenter: {first_display_name}")

        # 设置Item Editor的初始激活状态
        if self.item_editor_presenters:
            first_editor_name = next(iter(self.item_editor_presenters.keys()))
            self.active_item_editor_presenter = self.item_editor_presenters[first_editor_name]
            print(f"初始激活的Item Editor Presenter: {first_editor_name}")


    def refresh_and_distribute_display_data(self,selection_condition:SelectionCondition = None):
        """
        根据Model的签名
        分配他们给不同的模块
        初始化不同模块的数据

        注意！我不打算让Presenter拥有自己承载的是什么数据模型的数据
        因此，每次都要重新分发
        """
        if not selection_condition:
            # 如果没有提供选择条件且没有激活的context selection presenter，则跳过数据分发
            if not self.active_context_selection_presenter:
                print("警告: 没有激活的Context Selection Presenter，跳过数据分发")
                return
            selection_condition = self.active_context_selection_presenter.get_selection_condition()

        if not self.models:
            logging.warning("Capture-CapturePresenter-没有数据模型被接受")

        for _, model in self.models.items(): # 这个函数出问题了，model没有东西
            # 首先为每个模型加载数据
            model_data = self.data_service.parse_selection_condition(selection_condition)
            for display_name in model.item_displayable_list:
                # 加载数据
                rendered_data = model.renderer.render_all(model_data) # 获取chen
                self.item_display_presenters[display_name].fill_data(rendered_data) 

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
        return self.view.switch_to_tab(presenter_name)
                
    def initialize(self):
        return super().initialize()
    
    def shutdown(self):
        return super().shutdown()
    
    @property
    def name(self):
        return "capture_presenter"
    
    @property
    def view(self):
        return self._view