from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from ti.UI.rawUI.ui_InterventionCard import Ui_interventionWidget
from ti.UI.widgets.other.BasicButton import BasicButton
from ti.features.intervention.model.model import INV_State_Presentation, INVEvent

class InterventionCard(QWidget):
    button_clicked = pyqtSignal(INVEvent) 
    
    def __init__(
        self,
        title: str,
        choices: list,
        id,
        parent = None
        ):
        """_summary_

        Args:
            title (str): 干涉的标题
            choice (list): 干涉的选项
        """
        super().__init__(parent)
        self.ui = Ui_interventionWidget()
        self.ui.setupUi(self)
        
        # 初始化外观
        self.ui.title.setText(title)
        
        self.id = id
        
        self.buttons = {}
        
        for choice in choices:
            text = choices[choice]
            id = choice
            
            self.buttons[id] = BasicButton(self.ui.choiceWidget)
            self.buttons[id].setText(text)
            self.buttons[id].clicked.connect(lambda checked, c_id = id: self._on_button_clicked(c_id)) # TODO: 这里有问题
            
            self.ui.choiceLayout.addWidget(self.buttons[id]) 
        
        
    def _on_button_clicked(self, button_id: str):
        """
        这个槽函数现在接收按钮的ID字符串。
        它的新职责是：
        1. 将字符串ID转换为 INVEvent 枚举成员。
        2. 发射 button_clicked 信号，并把这个枚举成员传递出去。
        """
        print(f"卡片 '{self.id}' 上的按钮 '{button_id}' 被点击。")
        
        try:
            # 3. 将按钮ID字符串 (e.g., "choice_accept") 转换回 INVEvent 枚举
            event_to_emit = INVEvent(button_id)
            
            # 4. 发射信号，将转换后的 event 对象传递给连接的 Presenter
            self.button_clicked.emit(event_to_emit)
            
        except ValueError:
            # 如果 button_id 不是 INVEvent 中定义的值，会抛出 ValueError
            print(f"错误：按钮ID '{button_id}' 不是一个有效的 INVEvent。")
        
    def replace_titleText(self,text):
        self.ui.title.setText(text)
    
    def replace_buttonPlace(self,widgets:list):
        """
        清除布局中所有旧的按钮，并添加一组新的按钮。
        """
        # 1. 遍历当前存储的按钮字典，从布局中移除每一个旧的按钮控件
        for button_id in self.buttons:
            button_to_remove = self.buttons[button_id]
            self.ui.choiceLayout.removeWidget(button_to_remove)
            # 推荐：在移除后也将其父级设为None或删除，确保被垃圾回收
            button_to_remove.setParent(None) 
        
        # self.buttons 字典将在 apply_presentation 中被重置，这里只负责UI操作

        # 2. 将传入的新按钮控件列表添加到布局中
        for widget in widgets:
            self.ui.choiceLayout.addWidget(widget)
        
    def apply_presentation(self, presentation: INV_State_Presentation):
        """
        接收一个 Presentation "配方"对象，并将其应用到卡片UI上。
        
        这个方法会：
        1. 更新标题。
        2. 清除所有旧的按钮。
        3. 根据配方创建并显示新的按钮。
        """
        # 1. 使用辅助函数更新标题文本
        self.replace_titleText(presentation["title"])
        
        # 2. 准备创建新的按钮
        new_button_widgets = []
        
        # 在创建新按钮之前，先清空旧的按钮逻辑引用
        # replace_buttonPlace 会处理UI上的移除，这里处理逻辑上的清空
        self.buttons = {} 

        # 3. 遍历配方中的按钮数据，创建新的按钮实例
        button_recipe = presentation["buttons"]
        for button_id in button_recipe:
            button_text = button_recipe[button_id]
            # 创建一个新的 BasicButton 实例
            new_button = BasicButton(self.ui.choiceWidget)
            new_button.setText(button_text)
            
            # 使用 lambda 将按钮的唯一ID连接到点击事件的槽函数
            # 这是识别哪个按钮被点击的最佳实践
            new_button.clicked.connect(
                lambda checked, b_id=button_id: self._on_button_clicked(b_id)
            )
            
            # 将新创建的按钮添加到逻辑字典和UI widget列表中
            self.buttons[button_id] = new_button
            new_button_widgets.append(new_button)
            
        # 4. 使用辅助函数，用新创建的按钮列表替换掉旧的按钮
        self.replace_buttonPlace(new_button_widgets)
        
        

            
        
        
            
            
        

        