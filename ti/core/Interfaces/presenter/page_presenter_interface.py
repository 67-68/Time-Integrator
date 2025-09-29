from abc import ABC,abstractmethod

from ti.core.Interfaces.view.page_view_interface import IPageView
from ti.core.eventBus import EventBus
from ti.features.capture.model.mode_button import ModeBtn
from ti.model.events import PluginEvents
from ti.model.plugin.page_contributions import PageContribution
from ti.services.utils import QtABCMeta


class IPagePresenter(ABC, metaclass=QtABCMeta):
    """
    这个类用来表示Core内
    Presenter的Interface
    它掌管一个page，负责页面添加事宜

    Args:
        ABC (_type_): _description_
    """
    
    page: type[IPageView]
    page_contributions:dict[PageContribution]
    bus:EventBus
    
    @abstractmethod
    def initialize(self):
        """
        初始化方法
        """
        self.bus.subscribe(PluginEvents.PAGE_PLUGIN_CREATED.value,self._on_page_needed)
        self.page.page_first_clicked.connect(self._on_page_first_clicked)

    @abstractmethod
    def _on_page_needed(self, page_contributions: list[PageContribution]):
        for contribution in page_contributions:
            print(f"examine page contribution {contribution.page_id}")
            if contribution.parent_page == self.page.page_name:
                page_id = contribution.page_id
                self.page_contributions[page_id] = contribution

                # 应用page_contribution
                self.create_page_contribution(contribution)
    
    @abstractmethod
    def create_page_contribution(
        self,
        contribution:PageContribution
    ):
        self.create_button(contribution)
        
    @abstractmethod
    def create_button(
        self,
        contribution:PageContribution
    ):
        self.page.create_navigation_btn(
            ModeBtn(
                contribution.page_id,
                contribution.navigation_name
            )
        ) 
    
    @abstractmethod
    def _on_page_first_clicked(self, page_id):
        """处理页面首次点击事件，调用回调函数创建页面"""
        if page_id in self.page_contributions:
            contribution = self.page_contributions[page_id]
            if contribution.create_page_callback:
                # 调用回调函数创建页面
                page_widget = contribution.create_page_callback(page_id)
                if page_widget:
                    # 添加到stacked widget并存储
                    self.page.add_page_to_stack(page_id, page_widget)
                    # 切换到新创建的页面
                    print(f"switch to {page_id}")
                    print("*" * 141)
                    self.page.switch_to_page(page_id)
