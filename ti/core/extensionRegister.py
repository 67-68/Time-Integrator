from ti.core.Interfaces.Extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
import inspect

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
        

class DynamicExtensionLoader:
    def __init__(
        self,
        plugin_manager: ExtensionRegister, 
        services# ServiceContainer,由于不能循环import只能注释掉了
    ):
        self.plugin_manager = plugin_manager
        self.services = services

    def discover_and_register_plugins(self, extension_package):
        # ... 动态发现插件类的逻辑 ...
        for plugin_class in extension_package:
            try:
                # === 魔法发生在这里！===
                instance = self._create_plugin_instance_with_di(plugin_class)
                self.plugin_manager.regist_plugin(instance)
            except Exception as e:
                print(f"Failed to create plugin {plugin_class.__name__}: {e}")

    def _create_plugin_instance_with_di(self, plugin_class: type[ExtensionInterface]):
        """
        使用内省（introspection）来自动解析并注入依赖。
        """
        # 1. 获取构造函数的签名
        signature = inspect.signature(plugin_class.__init__)
        
        dependencies_to_inject = {}

        # 2. 遍历签名中的每一个参数
        for param in signature.parameters.values():
            if param.name == 'self':
                continue
            
            param_type = param.annotation # -> 这就是 EventBus, RealTimeMonitor 等类型

            # 3. 从服务容器中，按类型查找对应的服务实例
            service_instance = self.services.get_class_service(param_type)

            if service_instance:
                dependencies_to_inject[param.name] = service_instance
            else:
                raise Exception(f"Dependency '{param_type.__name__}' not found in service container.")

        # 4. 将解析出的依赖，作为关键字参数，传入构造函数来创建实例！
        print(f"Creating instance of {plugin_class.__name__} with dependencies: {list(dependencies_to_inject.keys())}")
        return plugin_class(**dependencies_to_inject)


        


    
        
        
        
    