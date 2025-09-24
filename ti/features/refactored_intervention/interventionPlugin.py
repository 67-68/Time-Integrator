from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.eventBus import EventBus
from ti.features.intervention.intervention_path_register import INV_PathRegister
from ti.model.plugin.path_register_provider_interface import IPathRegisterProvider


class InterventionPlugin(
    ExtensionInterface,
    IPathRegisterProvider
):
    def __init__(
        self,
    ):
        """_summary_
        这是Intervention插件的主类
        创建Coordinator之后完成
        插件应该是先于主体部分加载的
        """
        pass    
        
        
    
    # ------ 接口方法 ——----    
    
    @property
    def name(self):
        return "Intervention"
    
    def initialize(self, eventBus:EventBus):
        pass
    
    def shutdown(self):
        return super().shutdown()
    
    @staticmethod
    def register_class():
        return INV_PathRegister