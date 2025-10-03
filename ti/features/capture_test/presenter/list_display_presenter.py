from PyQt6.QtCore import QObject, pyqtSignal
from pydantic import BaseModel
from ti.features.capture.view.selection_view import SelectionView
from ti.features.capture_test.presenter.item_display_presenter_interface import IItemDisplayPresenter
from ti.model.action_unit import ActionUnit


class ListDisplayPresenter(IItemDisplayPresenter):
    item_selected = pyqtSignal(BaseModel) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._view = SelectionView()
        self.view.record_clicked.connect(self._on_item_selected)
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
    
    def fill_data(self, data: dict):
        """
        填充记录列表
        目前只有一个填充的流程
        在之后可能会加入排序
        """
        # 如果是一个列表
        if isinstance(data,dict):
            raise TypeError(f"ItemDisplayPresenter-fill_records: data input is a list instead of a dict: {data}")
        
        for name in data:
            if not hasattr(data[name],"uuid"):
                raise TypeError("ItemDisplayPresenter-fill_records: data model do not have attribute uuid")
            else:
                break
        
        self.data = {uuid:item for uuid,item in data.items()}
        
        # 清空现有记录
        self.view.record_list.clear()
        
        # 添加ActionUnit记录到列表
        for uuid,au in data.items():
            # 创建列表项并设置显示文本
            item_text = f"{au.action} ({au.start} - {au.end})"
            
            # 添加列表项并设置UserRole为ActionUnit对象
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(item_text)
            item.setData(1000, au)  # 使用UserRole存储ActionUnit对象
            
            self.view.record_list.addItem(item)
            
    @property    
    def view(self):
        return self._view
    
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