from abc import ABC,abstractmethod

from PyQt6.QtCore import pyqtSignal,QObject


from ti.services.utils import QtABCMeta
from ti.view.rawUI.ui_rawIPageView import Ui_main_page
from ti.view.widgets.other.BasicButton import BasicButton


class IPageView(ABC, metaclass=QtABCMeta):
    page_first_clicked: pyqtSignal
    
    """
    这个类作为所有核心界面的接口
    他们的共同点是：有一个名字，可以在界面栏中切换
    以及，可以检测插件对于页面的注册并获取这个被注册的页面

    Args:
        ABC (_type_): _description_
    """
    
    @property
    @abstractmethod
    def page_name(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self):
        """
        负责架设UI并删除pages
        """
        pass
    
    @abstractmethod
    def create_navigation_btn(self, btn_data):
        """
        创建导航按钮并添加到mode_change_frame
        """
        parent = self.page.mode_change_frame
        button = BasicButton(master = parent)
        button.setText(btn_data.text)
        button.setObjectName(f"btn_{btn_data.page_id}")
        button.clicked.connect(lambda: self._on_navigation_btn_clicked(btn_data.page_id))
        
        # 添加到mode_change_frame的verticalLayout_2中
        layout = self.page.mode_change_frame.layout()
        layout.insertWidget(layout.count() - 1, button)  # 在spacer之前插入
        
        return button

    @abstractmethod
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
            
    @abstractmethod
    def add_page_to_stack(self, page_id, page_widget):
        """
        添加页面到stacked widget并存储
        """
        self.pages[page_id] = page_widget
        self.page.stackedWidget.addWidget(page_widget)
    
    @abstractmethod
    def switch_to_page(self, page_id):
        """
        切换到指定页面
        """
        if page_id in self.pages:
            page_widget = self.pages[page_id]
            self.page.stackedWidget.setCurrentWidget(page_widget)