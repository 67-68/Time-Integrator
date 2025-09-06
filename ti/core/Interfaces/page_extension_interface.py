from abc import ABC,abstractmethod
from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.page_contributions import PageContribution


class PageExtensionInterface(ExtensionInterface): #这里还需要继承ABC吗？
    @property
    @abstractmethod
    def page_contributions(self) -> list[PageContribution]:
        """
        用来存储这个类有什么自定义的界面
        以及它们会被放到哪里

        Returns:
            list[PageContribution]: _description_
        """
        pass
    
    @abstractmethod
    def create_page(self):
        """
        用来创建插件自己的page
        无论使用工厂还是就地创建
        """
        pass
    
