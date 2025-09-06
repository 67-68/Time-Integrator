# 这是插件capture的presenter, 不是capturePage核心的presenter
from PyQt6.QtCore import QObject

from ti.features.capture.view.capture_widget import CaptureWidget
from ti.services.dataAccess.dataService import DataService
from ti.core.eventBus import EventBus
from ti.model.action_unit import ActionUnit


class CapturePresenter(QObject):
    """
    CapturePresenter管理capture插件的业务逻辑
    协调UI组件和数据服务
    """
    
    def __init__(self, data_service: DataService, event_bus: EventBus):
        super().__init__()
        self.data_service = data_service
        self.event_bus = event_bus
        
        # 创建UI组件
        self.widget = CaptureWidget()
        
        # 连接信号
        self.connect_signals()
        
        # 初始化数据
        self.initialize_data()
        
    def connect_signals(self):
        """连接信号"""
        # UI信号连接
        self.widget.actionUnitCreated.connect(self._on_action_unit_created)
        self.widget.actionUnitSelected.connect(self._on_action_unit_selected)
        self.widget.dateChanged.connect(self._on_date_changed)
        
        # 数据服务信号连接
        if hasattr(self.data_service, 'actionUnit_added'):
            self.data_service.actionUnit_added.connect(self._on_data_service_action_unit_added)
            
    def initialize_data(self):
        """初始化数据"""
        # 获取今天的日期
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 加载今天的数据
        self.load_date_data(today)
        
    def load_date_data(self, date_str: str):
        """加载指定日期的数据"""
        try:
            # 从数据服务获取数据
            date_data = self.data_service.get_date_data(date_str)
            
            # 填充到UI
            self.widget.fill_date_data(date_data)
            self.widget.set_current_date(date_str)
            
        except Exception as e:
            print(f"Failed to load date data for {date_str}: {e}")
            
    def _on_action_unit_created(self, action_unit: ActionUnit):
        """处理ActionUnit创建事件"""
        try:
            # 保存到数据服务
            current_date = self.widget.current_date or self._get_today_string()
            self.data_service.add_actionUnit(current_date, action_unit)
            
            # 发布事件
            self.event_bus.publish("ActionUnitCreated", {
                'date': current_date,
                'action_unit': action_unit
            })
            
        except Exception as e:
            print(f"Failed to create action unit: {e}")
            
    def _on_action_unit_selected(self, action_unit: ActionUnit):
        """处理ActionUnit选择事件"""
        # 可以在这里处理选择逻辑，比如更新其他UI组件
        pass
        
    def _on_date_changed(self, date_str: str):
        """处理日期改变事件"""
        self.load_date_data(date_str)
        
    def _on_data_service_action_unit_added(self, action_unit: ActionUnit):
        """处理数据服务添加ActionUnit事件"""
        # 刷新当前日期数据
        if self.widget.current_date:
            self.load_date_data(self.widget.current_date)
            
    def _get_today_string(self) -> str:
        """获取今天的日期字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def getWidget(self) -> CaptureWidget:
        """获取UI组件"""
        return self.widget
        
    def shutdown(self):
        """关闭presenter，清理资源"""
        # 这里可以进行清理工作
        pass