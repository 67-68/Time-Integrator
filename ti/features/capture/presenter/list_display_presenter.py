from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QListWidgetItem, QVBoxLayout
from pydantic import BaseModel
from ti.features.capture.view.record_list import RecordList
from ti.features.capture.view.selection_view import SelectionView
from ti.features.capture.presenter.item_display_presenter_interface import IItemDisplayPresenter
from ti.model.action_unit import ActionUnit
from ti.view.BasicFrame import BasicFrame


class ListDisplayPresenter(IItemDisplayPresenter):
    item_selected = pyqtSignal(BaseModel) 
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建RecordList并用BasicFrame封装
        self._record_list = RecordList()
        self._frame = BasicFrame()

        # 设置布局
        layout = QVBoxLayout(self._frame)
        layout.addWidget(self._record_list)
        self._frame.setLayout(layout)

        # 连接信号
        self._record_list.record_clicked.connect(self._on_item_selected)
        self.data = None

    def initialize(self):
        return super().initialize()
    
    def shutdown(self):
        return super().shutdown()
    
    def _on_item_selected(self,action_unit):
        """处理记录项点击事件"""
        print(f"Record selected: {action_unit.action}")
        # 发射信号到capture presenter
        self.item_selected.emit(action_unit)
    
    def fill_data(self, data):
        """
        填充记录列表
        接受QListWidgetItem列表

        Args:
            data: QListWidgetItem列表
        """
        # 清空现有记录
        self._record_list.clear()

        # 检查数据类型
        if not isinstance(data, list):
            raise TypeError(f"ListDisplayPresenter-fill_data: 输入必须是列表，而不是 {type(data)}")

        # 直接添加预创建的QListWidgetItem
        for item in data:
            if isinstance(item, QListWidgetItem):
                self._record_list.addItem(item)
            else:
                raise TypeError(f"ListDisplayPresenter-fill_data: 列表中的元素不是QListWidgetItem: {type(item)}")
            
    @property
    def view(self):
        return self._frame
    
    def add_data(self, model_data):
        """
        增加一个data到本地存储并重新渲染数据

        Args:
            model_data (_type_): _description_
        """
        if not hasattr(model_data,"uuid"):
            raise TypeError(f"{self.__class__}-add_data: model_data do not have attribute uuid: {model_data}")
        
        self.data[model_data.uuid] = model_data
        
        self.fill_data(self.data)
        
    @property
    def name(self):
        return "list_display_presenter"