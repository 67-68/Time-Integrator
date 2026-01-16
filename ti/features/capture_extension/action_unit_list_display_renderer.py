from ti.features.capture.service.capture_factory_interface import ICaptureRenderer
from PyQt6.QtWidgets import QListWidgetItem
from ti.model.action_unit import ActionUnit
import logging

class ActionUnitListRenderer(ICaptureRenderer):
    def __init__(self):
        pass
    
    def render_all(self, data: list):
        """
        渲染所有ActionUnit数据为QListWidgetItem列表

        Args:
            data: ActionUnit对象列表

        Returns:
            list: QListWidgetItem列表
        """
        if not isinstance(data, list):
            logging.error(f"{__name__}: data is not list, can not render")
            return []

        datalist = []
        for d in data:
            rendered_item = self.render_model(d)
            if rendered_item:
                datalist.append(rendered_item)

        return datalist

    def render_model(self, action_unit: ActionUnit):
        """
        渲染单个ActionUnit为QListWidgetItem

        Args:
            action_unit: ActionUnit对象

        Returns:
            QListWidgetItem: 渲染后的列表项
        """
        if not isinstance(action_unit, ActionUnit):
            logging.error(f"{__name__}: render_model expects ActionUnit, got {type(action_unit)}")
            return None

        # 创建列表项并设置显示文本
        item_text = f"{action_unit.action} ({action_unit.start} - {action_unit.end})"

        # 创建QListWidgetItem并设置UserRole为ActionUnit对象
        item = QListWidgetItem(item_text)
        item.setData(1000, action_unit)  # 使用UserRole存储ActionUnit对象

        return item
        