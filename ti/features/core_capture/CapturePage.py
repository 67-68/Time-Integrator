
from PyQt6.QtCore import pyqtSignal

from ti.core.eventBus import EventBus
from ti.model.action_unit import ActionUnit

from ti.model.events import PluginEvents
from ti.model.page_contributions import PageContribution
from ti.view.rawUI.ui_rawNewCapturePage import Ui_NewCapturePage
from ti.view.widgets.other.BasicButton import BasicButton
from ti.view.widgets.pages.BasicWidget import BasicWidget



class New_CapturePage(BasicWidget):
    page_first_clicked = pyqtSignal(str)
    
    def __init__(
        self,
        parent = None
    ):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.CP = Ui_NewCapturePage()
        self.CP.setupUi(self)
        
        # 删除默认的pages
        while self.CP.stackedWidget.count() > 0:
            widget = self.CP.stackedWidget.widget(0)
            self.CP.stackedWidget.removeWidget(widget)
            
        self.pages = {}
    
            
    def create_navigation_btn(self, btn_data):
        """
        创建导航按钮并添加到mode_change_frame
        """
        parent = self.CP.mode_change_frame
        button = BasicButton(master = parent)
        button.setText(btn_data.text)
        button.setObjectName(f"btn_{btn_data.page_id}")
        button.clicked.connect(lambda: self._on_navigation_btn_clicked(btn_data.page_id))
        
        # 添加到mode_change_frame的verticalLayout_2中
        layout = self.CP.mode_change_frame.layout()
        layout.insertWidget(layout.count() - 1, button)  # 在spacer之前插入
        
        return button
    
    def _on_navigation_btn_clicked(self, page_id):
        """
        导航按钮点击事件处理
        """
        print(f"Navigation button clicked: {page_id}")
        
        if page_id in self.pages:
            # 如果页面已存在，直接切换
            self.switch_to_page(page_id)
        else:
            # 如果页面不存在，发送首次点击信号
            self.page_first_clicked.emit(page_id)
    
    def add_page_to_stack(self, page_id, page_widget):
        """
        添加页面到stacked widget并存储
        """
        self.pages[page_id] = page_widget
        self.CP.stackedWidget.addWidget(page_widget)
    
    def switch_to_page(self, page_id):
        """
        切换到指定页面
        """
        if page_id in self.pages:
            page_widget = self.pages[page_id]
            self.CP.stackedWidget.setCurrentWidget(page_widget)