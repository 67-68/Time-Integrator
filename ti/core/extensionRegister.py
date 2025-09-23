from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.plugin.function_provider_interface import IFunctionExtension
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.model.plugin.path_register_provider_interface import IPathRegisterProvider
from ti.model.plugin.symbol_path_register_interface import ISymbolPathRegister
from ti.core.eventBus import EventBus
import inspect

from ti.model.events import PluginEvents
from ti.services.function_service import FunctionService
from ti.services.symbol_service import SymbolService

class ExtensionRegister:
    def __init__(
        self,
        eventBus:EventBus,
        
    ):
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
        print("=" * 10)
        print(f"initilizing plugin {plugin.name}")
        plugin.initialize(self.eventBus)
        print("sucessfully intitialize")
        print("=" * 10)
        
        
        self.plugins[name] = plugin
        

class DynamicExtensionLoader:
    def __init__(
        self,
        plugin_manager: ExtensionRegister, 
        services, # ServiceContainer,由于不能循环import只能注释掉了
        bus: EventBus,
        symbol_service: SymbolService,
        function_service: FunctionService
    ):
        self.plugin_manager = plugin_manager
        self.services = services
        self.bus = bus
        self.symbol = symbol_service
        self.registers = {}
        self.function_service = function_service
        

    def discover_and_register_plugins(self, extension_package):
        # 首先加载插件的symbol_register
        print("=" * 20)
        print("[LOADER]Searching for symbol register in plugins...")
        for plugin_class in extension_package:    
            if (hasattr(plugin_class, 'register_class') and 
                issubclass(plugin_class, IPathRegisterProvider)):
                    print(f"find {plugin_class.name}")
                    # 调用静态方法获取register类
                    register_class = plugin_class.register_class()
                    # 创建register实例并注册
                    register_instance = register_class()
                    self.symbol.regist_register(register_instance)
                    print(f"successfully regist symbol path register for plugin {plugin_class.name} ")
            

                    
        # ... 动态发现插件类的逻辑 ...
        for plugin_class in extension_package:
            try:
                # === 魔法发生在这里！===
                instance = self._create_plugin_instance_with_di(plugin_class)
                self.plugin_manager.regist_plugin(instance)
                
                # pages
                print("[LOADER]Searching for page contribution in plugins...")   
                if isinstance(instance,IPageExtension):
                    pages = instance.page_contributions
                    print(f"found page contribution: {pages}")
                    self.bus.publish(PluginEvents.PAGE_PLUGIN_CREATED.value, pages)
                
                # 查看是否存在功能提供
                print("[LOADER]Searching for function contribution in plugins...")   
                if isinstance(instance, IFunctionExtension):
                    print(f"find {plugin_class.name}")
                    contributions = instance.function_contributions
                    # 注册函数
                    for contribution in contributions:
                        self.function_service.regist_function(contribution)
                    
                    print(f"successfully find functions register for plugin {plugin_class.name} ")
                
            except Exception as e:
                print(f"Failed to create plugin {plugin_class.__name__}: {e}")
                import traceback
                traceback.print_exc()

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
            try:
                service_instance = self.services.get_class_service(param_type)
            except KeyError:
                service_instance = None

            if service_instance:
                dependencies_to_inject[param.name] = service_instance
            else:
                available_services = list(self.services._services.keys())
                available_service_names = [s.__name__ if hasattr(s, '__name__') else str(s) for s in available_services]
                raise Exception(f"Dependency '{param_type.__name__}' not found in service container. Available services: {available_service_names}")

        # 4. 将解析出的依赖，作为关键字参数，传入构造函数来创建实例！
        print(f"Creating instance of {plugin_class.__name__} with dependencies: {list(dependencies_to_inject.keys())}")
        return plugin_class(**dependencies_to_inject)   
    
    def get_registers(self) -> list[type[ISymbolPathRegister]]:
        return self.registers
        


    
        
        
        
    