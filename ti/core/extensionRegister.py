from ti.core.Interfaces.Extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus


class ExtensionRegister:
    def __init__(self,eventBus:EventBus):
        """
        这个类用于注册和管理插件
        同时为他们提供第一推动力
        """
        self.plugins = {}
        self.eventBus = eventBus
        
    def regist_plugin(self,plugin:ExtensionInterface):
        """_summary_
        把插件注册到主要的系统中
        需要一个插件实例
        Args:
            plugin (_type_): 插件主类实例
        """
        name = plugin.name
        plugin.initialize(self.eventBus)
        self.plugins[name] = plugin
    
        
        
        
    