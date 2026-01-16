from abc import ABC, abstractmethod


class ICaptureRenderer(ABC):
    """
    作为Capture功能数据模型RenderAbleItemModel的一部分
    它被用来输入数据模型
    创建渲染过的东西
    然后被直接添加进View
    """
    @abstractmethod
    def render_model(self):
        pass
    
    @abstractmethod
    def render_all(self):
        pass