# 这是插件capture的presenter, 不是capturePage核心的presenter
from PyQt6.QtCore import QObject

from ti.features.capture.presenter.selection_presenter import CAP_SelectionPresenter
from ti.features.capture.presenter.input_presenter import CAP_InputPresenter
from ti.features.capture.view.capture import CaptureView
from ti.features.detector.service.matchers import get_time_from_str
from ti.services.dataService import DataService
from ti.core.eventBus import EventBus
from ti.model.action_unit import ActionUnit
import uuid


class CapturePresenter(QObject):
    """
    CapturePresenter管理capture插件的业务逻辑
    协调UI组件和数据服务
    """
    
    def __init__(
        self,
        data_service: DataService,
        event_bus: EventBus,
        selection: CAP_SelectionPresenter,
        input: CAP_InputPresenter,
    ):
        super().__init__()
        self.data_service = data_service
        self.event_bus = event_bus
        
        # 管理presenter
        self.selection = selection
        self.input = input
        self.input.initialize()
        
        # 创建主视图并设置布局
        self.widget = CaptureView()
        self._setup_view_layout()
        
    def _setup_view_layout(self):
        """设置视图布局 - 左边selection view, 右边input view"""
        # 获取子presenter的view
        selection_view = self.selection.view
        input_view = self.input.get_widget()
        
        # 添加到主视图
        self.widget.add_selection_view(selection_view)
        self.widget.add_input_view(input_view)
        
        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        """连接所有信号"""
        # 连接selection presenter的日期选择信号
        self.selection.date_selected.connect(self._on_date_selected)
        # 连接selection presenter的记录选择信号
        self.selection.record_selected.connect(self._on_record_selected)
        
        # 连接input presenter的保存和新建信号
        self.input.save_requested.connect(self._on_save_requested)
        self.input.new_requested.connect(self._on_new_requested)
        self.input.delete_requested.connect(self._on_delete_requested)
        
    def _on_date_selected(self, date_str):
        """处理日期选择事件"""
        print(f"Capture presenter received date: {date_str}")
        # 从dataService获取当天数据
        action_units = self.data_service.get_date_data(date_str)
        self.date = date_str
        # 填充记录列表
        self.fill_records(action_units)
        
    def fill_records(self, action_units):
        """填充记录列表"""
        # 调用selection presenter的同名函数
        self.selection.fill_records(action_units)
        
    def _on_save_requested(self, property_data):
        """
        处理保存请求
        :param property_data: 属性数据字典
        """ # 这里不能创建，按理来说存储用的就应该是actionUnit, 而不是字典
        # 创建ActionUnit对象
        action_unit = ActionUnit(
            id=str(uuid.uuid4()),
            date=self._get_current_date(),
            action=property_data.get('action', ''),
            start=property_data.get('start', ''),
            end=property_data.get('end', ''),
            action_type=property_data.get('action_type', ''),
            action_detail=property_data.get('action_detail', ''),
            timeSpan=self._calculate_time_span(property_data.get('start', ''), property_data.get('end', '')), #TOOD: 这里出问题了
            urgency=property_data.get('is_urgent', False),
            importance=property_data.get('is_important', False)
        )
        
        # 保存到数据服务
        self.data_service.add_actionUnit(action_unit)
        
        # 刷新各个widget
        self._refresh_all_widgets()
        
        # 重置删除计数器
        self.input.button_group.reset_delete_count()
    
    def _on_record_selected(self, action_unit):
        """
        处理记录项选择事件
        :param action_unit: 选中的ActionUnit对象
        """
        print(f"Capture presenter received action unit: {action_unit.action}")
        # 将ActionUnit转换为property_data字典并填充到input presenter
        self._refresh_input_presenter(action_unit)
    
    def _on_new_requested(self):
        """处理新建请求"""
        # 获取新的action unit
        new_action_unit = self.data_service.createNewData()
        
        # 刷新input presenter（不清空selection presenter）
        self._refresh_input_presenter(new_action_unit)
        
        # 重置删除计数器
        self.input.button_group.reset_delete_count()
    
    def _on_delete_requested(self, property_data):
        """
        处理删除请求
        :param property_data: 属性数据字典
        """
        current_date = self._get_current_date()
        start_time = property_data.get('start', '')
        
        if current_date and start_time:
            # 根据日期和开始时间查找ActionUnit
            action_unit = self.data_service.find_action_unit_by_date_and_start(current_date, start_time)
            if action_unit:
                # 使用UUID删除ActionUnit
                self.data_service.delete_actionUnit(action_unit.id)
                print(f"删除ActionUnit: {action_unit.id}")
                
                # 刷新界面
                self._refresh_all_widgets()
                
                # 重置删除计数器
                self.input.button_group.reset_delete_count()
    
    def _get_current_date(self):
        """获取当前日期"""
        return self.date
    
    def _calculate_time_span(self, start_time, end_time):
        """计算时间跨度"""
        # 这里需要实现时间跨度计算逻辑
        return get_time_from_str(end_time) - get_time_from_str(start_time)
    
    def _refresh_all_widgets(self):
        """刷新所有widget"""
        # 刷新selection presenter
        current_date = self._get_current_date()
        if current_date:
            action_units = self.data_service.get_date_data(current_date)
            self.fill_records(action_units)
        
        # 刷新input presenter（清空输入）
        self._refresh_input_presenter(None)
    
    def _refresh_input_presenter(self, action_unit):
        """刷新input presenter"""
        # 清空或设置input presenter的数据
        if action_unit:
            # 设置action unit数据到property view
            property_data = {
                'start': action_unit.start,
                'end': action_unit.end,
                'action_type': action_unit.action_type,
                'action': action_unit.action,
                'action_detail': action_unit.action_detail,
                'is_urgent': action_unit.urgency,
                'is_important': action_unit.importance
            }
            # 通过input presenter的view访问property view
            self.input.input_view.property_view.set_property_data(property_data)
        else:
            # 清空输入
            self.input.input_view.property_view.clear_properties()
            self.input.input_view.smart_input_view.clear_text()
    
        