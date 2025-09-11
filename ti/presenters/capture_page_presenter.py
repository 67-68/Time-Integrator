from ti.core.eventBus import EventBus
from ti.features.capture.model.mode_button import CaptureModeBtn
from ti.features.core_capture.CapturePage import New_CapturePage
from ti.model.core_pages import CoreView
from ti.model.events import PluginEvents
from ti.model.page_contributions import PageContribution



class CapturePagePresenter:
    def __init__(
        self,
        capture_page: New_CapturePage,
        bus: EventBus
    ):
        """
        这个presenter用来管理capturePage
        监听插件生成，检查是否有创建页面的请求
        """
        self.page = capture_page
        self.page_contributions = {}
        self.bus = bus
        
            # 监听需要页面创建的插件
        self.bus.subscribe(PluginEvents.PAGE_PLUGIN_CREATED.value,self._on_page_needed)
        
        # 连接页面首次点击信号
        self.page.page_first_clicked.connect(self._on_page_first_clicked)
    
    def _on_page_needed(self, page_contributions: list[PageContribution]):
        for contribution in page_contributions:
            print(f"examine page contribution {contribution.page_id}")
            if contribution.parent_page == CoreView.CAPTURE_PAGE.value:
                page_id = contribution.page_id
                self.page_contributions[page_id] = contribution

                # 应用page_contribution
                self.create_page_contribution(contribution)
    
    def create_page_contribution(
        self,
        contribution:PageContribution
    ):
        self.create_button(contribution)
        
    def create_button(
        self,
        contribution:PageContribution
    ):
        self.page.create_navigation_btn(
            CaptureModeBtn(
                contribution.page_id,
                contribution.navigation_name
            )
        ) 
    
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
                    print(f"[CAP]switch to {page_id}")
                    self.page.switch_to_page(page_id)
