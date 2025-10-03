"""
验收测试：捕获插件 (Capture Plugin)

这个测试验证捕获插件的主要功能，包括：
1. 插件初始化
2. Presenter创建和配置
3. 视图集成
4. 数据流处理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pluggy import PluginManager
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from PyQt6.QtWidgets import QApplication

from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister
from ti.features.capture_test.capture_plugin import TESTCapturePlugin
from ti.features.capture_test.presenter.capture_presenter import CapturePresenter
from ti.features.capture_test.presenter.context_selection_presenter import ContextSelectionPresenter
from ti.features.capture_test.presenter.list_display_presenter import ListDisplayPresenter
# 使用Mock替代ItemEditorPresenter，因为实际类名是ActionUnitEditorPresenter
from unittest.mock import Mock
from ti.core.eventBus import EventBus
from ti.services.dataService import DataService
from ti.services.function_service import FunctionService
from ti.services.serviceContainer import ServiceContainer
from ti.services.symbol_service import SymbolService
from ti.services.strategy_service import StrategyService
from ti.model.action_unit import ActionUnit


class TestCapturePluginAcceptance:
    """捕获插件验收测试"""

    def setup_method(self):
        """测试方法前的设置"""
        # 在测试环境中初始化QApplication
        if not QApplication.instance():
            self.app = QApplication([])

        # 创建模拟的服务对象
        self.bus = EventBus()
        self.container = ServiceContainer()
        self.ER = self.container.getService("ER")
        self.symbol = self.container.getService("symbol")
        self.function = self.container.getService("function")
        self.data_service = Mock(spec=DataService)
        self.translator = Mock()

        self.loader = DynamicExtensionLoader(
            self.ER,
            self.container,
            self.bus,
            self.symbol,
            self.function
        )

    def test_plugin_initialization(self):
        """测试插件初始化过程"""
        # 创建插件实例
        plugin = TESTCapturePlugin(self.data_service, self.translator)

        # 验证插件基本属性
        assert plugin.name == "capture_plugin_test"
        assert plugin.data_service == self.data_service
        assert plugin.translator == self.translator

        # 初始化插件
        plugin.initialize(self.bus)

        # 验证事件总线已设置
        assert plugin.event_bus == self.bus

        # 验证页面贡献
        page_contributions = plugin.page_contributions
        assert len(page_contributions) == 1

        capture_page = page_contributions[0]
        assert capture_page.page_id == "capture_plugin_page_test"
        assert capture_page.navigation_name == "输入行动_test"
        assert capture_page.parent_page == "capture_page"
        assert capture_page.create_page_callback == plugin.create_page

    @patch('ti.services.strategy_service.StrategyService.execute_strategies_from_protocol')
    @patch('ti.services.strategy_service.StrategyService.get_strategy_methods_from_protocol')
    @patch('ti.services.strategy_service.StrategyService.execute_with_strategy')
    def test_create_capture_view(self, mock_execute_with_strategy, mock_get_strategies, mock_execute_strategies):
        """测试创建捕获视图"""
        # 设置模拟返回值
        mock_context_presenters = [Mock(spec=ContextSelectionPresenter)]
        mock_editor_presenters = [Mock()]  # 使用通用Mock替代ItemEditorPresenter
        mock_display_presenters = [Mock(spec=ListDisplayPresenter)]
        mock_data_models = [Mock()]

        mock_execute_strategies.side_effect = [
            mock_context_presenters,
            mock_editor_presenters,
            mock_display_presenters
        ]
        mock_get_strategies.return_value = mock_data_models

        # 创建模拟的presenter和view
        mock_presenter = Mock(spec=CapturePresenter)
        mock_view = Mock()
        mock_presenter.view = mock_view
        mock_execute_with_strategy.return_value = mock_presenter

        # 创建插件并测试
        plugin = TESTCapturePlugin(self.data_service, self.translator)
        plugin.initialize(self.bus)

        # 调用创建视图方法
        result_view = plugin.create_capture_view()

        # 验证策略服务调用
        assert mock_execute_strategies.call_count == 3
        mock_execute_strategies.assert_any_call(Mock, ContextSelectionPresenter)
        mock_execute_strategies.assert_any_call(Mock)
        mock_execute_strategies.assert_any_call(Mock)

        mock_get_strategies.assert_called_once_with(Mock)

        # 验证presenter创建
        mock_execute_with_strategy.assert_called_once()

        # 验证presenter引用被存储
        assert plugin.presenter == mock_presenter

        # 验证返回的视图
        assert result_view == mock_view

    def test_plugin_shutdown(self):
        """测试插件关闭过程"""
        plugin = TESTCapturePlugin(self.data_service, self.translator)
        plugin.initialize(self.bus)

        # 创建模拟presenter
        mock_presenter = Mock(spec=CapturePresenter)
        plugin.presenter = mock_presenter

        # 关闭插件
        plugin.shutdown()

        # 验证presenter被关闭
        mock_presenter.shutdown.assert_called_once()
        assert plugin.presenter is None

    def test_create_page_method(self):
        """测试创建页面方法"""
        plugin = TESTCapturePlugin(self.data_service, self.translator)
        plugin.initialize(self.bus)

        # 测试创建捕获页面
        with patch.object(plugin, 'create_capture_view') as mock_create_capture:
            mock_view = Mock()
            mock_create_capture.return_value = mock_view

            result = plugin.create_page("capture_plugin_page_test")

            mock_create_capture.assert_called_once()
            assert result == mock_view

        # 测试未知页面ID
        result = plugin.create_page("unknown_page")
        assert result is None

    @patch('ti.services.strategy_service.StrategyService.execute_strategies_from_protocol')
    def test_data_flow_integration(self, mock_execute_strategies):
        """测试数据流集成"""
        # 设置模拟presenter
        mock_context_presenter = Mock(spec=ContextSelectionPresenter)
        mock_editor_presenter = Mock()  # 使用通用Mock替代ItemEditorPresenter
        mock_display_presenter = Mock(spec=ListDisplayPresenter)

        mock_execute_strategies.side_effect = [
            [mock_context_presenter],
            [mock_editor_presenter],
            [mock_display_presenter]
        ]

        # 模拟数据服务返回
        mock_action_units = [
            ("uuid1", ActionUnit(
                id="uuid1",
                date="2024-01-01",
                start="09:00",
                end="10:00",
                action="测试行动",
                action_type="工作",
                action_detail="测试详情",
                urgency=False,
                importance=True
            ))
        ]
        self.data_service.get_date_data.return_value = mock_action_units

        # 创建插件和视图
        plugin = TESTCapturePlugin(self.data_service, self.translator)
        plugin.initialize(self.bus)

        with patch('ti.services.strategy_service.StrategyService.get_strategy_methods_from_protocol') as mock_get_strategies, \
             patch('ti.services.strategy_service.StrategyService.execute_with_strategy') as mock_execute_with_strategy:

            mock_get_strategies.return_value = [Mock()]
            mock_presenter = Mock(spec=CapturePresenter)
            mock_presenter.view = Mock()
            mock_execute_with_strategy.return_value = mock_presenter

            # 创建视图
            view = plugin.create_capture_view()

            # 验证presenter被正确创建
            assert plugin.presenter == mock_presenter
            assert view == mock_presenter.view


if __name__ == "__main__":
    # 运行验收测试
    pytest.main([__file__, "-v"])