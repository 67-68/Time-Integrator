"""
验收测试：干预插件 (Intervention Plugin)

这个测试验证干预插件的主要功能，包括：
1. 插件初始化
2. 项目创建和配置
3. 事件源和视图的集成
4. 用户交互流程
"""

from pluggy import PluginManager
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from PyQt6.QtWidgets import QApplication
import sys

from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister
from ti.features.detector.detector_plugin import DetectorPlugin
from ti.features.intervention.intervention_plugin import InterventionPlugin
from ti.core.eventBus import EventBus
from ti.features.intervention.inv_coordinator import INVCoordinator
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.function_service import FunctionService
from ti.services.serviceContainer import ServiceContainer
from ti.services.symbol_service import SymbolService
from ti.model.yaml_repository import YamlRepository


class TestInterventionPluginAcceptance:
    """干预插件验收测试"""
    
    def setup_method(self):
        """测试方法前的设置"""
        # 在测试环境中初始化QApplication
        if not QApplication.instance():
            self.app = QApplication([])
        
        # 创建模拟的服务对象
        bus = EventBus()
        container = ServiceContainer()
        ER = container.getService("ER")
        symbol = container.getService("symbol")
        function = container.getService("function")
        
        self.loader = DynamicExtensionLoader(
            ER,
            container,
            bus,
            symbol,
            function
        )
        
    def test_plugin_initialization(self):
        """测试插件初始化过程"""
        self.loader.discover_and_register_plugins([DetectorPlugin,InterventionPlugin])
        
        manager = self.loader.plugin_manager
        plugins = manager.plugins
        
        
        assert "Intervention" in plugins
        
        # 插件被初始化
        intervention:InterventionPlugin = plugins["Intervention"]
        
        # 生成了Project
        assert intervention.coordinator.projects != None

if __name__ == "__main__":
    # 运行验收测试
    pytest.main([__file__, "-v"])