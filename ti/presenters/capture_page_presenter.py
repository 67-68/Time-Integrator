from ti.view.views.capture import CapturePage


class CapturePagePresenter:
    def __init__(
        self,
        capture_page: CapturePage
    ):
        """
        这个presenter用来管理capturePage
        监听插件生成，检查是否有创建页面的请求
        """
        