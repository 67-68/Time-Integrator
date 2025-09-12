from PyQt6.QtCore import QObject, pyqtSignal
from ti.features.capture.view.selection_view import SelectionView


class CAP_SelectionPresenter(QObject):
    date_selected = pyqtSignal(str)  # 信号：日期被选择，传递日期字符串
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = SelectionView()
        self.connect_signals()
    
    def connect_signals(self):
        """连接信号"""
        # 连接日历的日期选择信号
        self.view.calendar.date_selected.connect(self._on_date_selected)
    
    def _on_date_selected(self, date_str):
        """处理日期选择事件"""
        print(f"Date selected: {date_str}")
        # 发射信号到capture presenter
        self.date_selected.emit(date_str)
    
    def fill_records(self, action_units):
        """填充记录列表"""
        # 清空现有记录
        self.view.record_list.clear()
        
        # 添加ActionUnit记录到列表
        for au in action_units:
            # 创建ActionUnit对象（如果传入的是字典）
            if isinstance(au, dict):
                au = ActionUnit.from_dict(au)
            
            # 创建列表项并设置显示文本
            item_text = f"{au.action} ({au.start} - {au.end})"
            
            # 添加列表项并设置UserRole为ActionUnit对象
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(item_text)
            item.setData(1000, au)  # 使用UserRole存储ActionUnit对象
            
            self.view.record_list.addItem(item)