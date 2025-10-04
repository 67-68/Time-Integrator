from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.features.capture_extension.strategy import CaptureExtensionStrategies
from ti.model.strategy.strategy_contribution import StrategyContribution
from ti.model.strategy.strategy_provider_interface import IStrategyProvider


class CaptureExtensionPlugin(IStrategyProvider,ExtensionInterface):
    def __init__(self):
        pass
    
    @property
    def strategy_contribution(self):
        contri = StrategyContribution(
            "capture_extension_strategy",
            CaptureExtensionStrategies
        )
        
        return contri
        
    @property
    def name(self):
        return "capture_extension"
    
    def initialize(self, eventBus):
        return super().initialize(eventBus)
    
    def shutdown(self):
        return super().shutdown()