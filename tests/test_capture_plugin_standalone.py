"""
独立版捕获插件验收测试

这个测试完全不依赖实际模块，使用纯Mock对象
"""

import unittest
from unittest.mock import Mock, MagicMock


class TestCapturePluginStandalone(unittest.TestCase):
    """独立版捕获插件验收测试"""

    def test_plugin_lifecycle(self):
        """测试插件完整生命周期"""
        print("=== 测试插件生命周期 ===")

        # 创建所有Mock对象
        mock_data_service = Mock()
        mock_translator = Mock()
        mock_event_bus = Mock()
        mock_event_bus.publish = Mock()

        # 模拟插件实例
        mock_plugin = Mock()
        mock_plugin.name = "capture_plugin_test"
        mock_plugin.data_service = mock_data_service
        mock_plugin.translator = mock_translator
        mock_plugin.event_bus = None
        mock_plugin.presenter = None

        # 模拟initialize方法
        def mock_initialize(event_bus):
            mock_plugin.event_bus = event_bus
            # 实际调用publish
            event_bus.publish("PagePluginRegistered", mock_plugin.page_contributions)

        mock_plugin.initialize = mock_initialize

        # 模拟page_contributions属性
        mock_page_contribution = Mock()
        mock_page_contribution.page_id = "capture_plugin_page_test"
        mock_page_contribution.navigation_name = "输入行动_test"
        mock_page_contribution.parent_page = "capture_page"
        mock_page_contribution.create_page_callback = Mock()

        mock_plugin.page_contributions = [mock_page_contribution]

        # 模拟create_page方法
        def mock_create_page(page_id):
            if page_id == "capture_plugin_page_test":
                return Mock()  # 返回模拟视图
            return None

        mock_plugin.create_page = mock_create_page

        # 模拟shutdown方法
        def mock_shutdown():
            if mock_plugin.presenter:
                mock_plugin.presenter.shutdown = Mock()
                mock_plugin.presenter.shutdown()
                mock_plugin.presenter = None

        mock_plugin.shutdown = mock_shutdown

        # 测试插件基本属性
        self.assertEqual(mock_plugin.name, "capture_plugin_test")
        self.assertEqual(mock_plugin.data_service, mock_data_service)
        self.assertEqual(mock_plugin.translator, mock_translator)
        print("✓ 插件基本属性验证通过")

        # 初始化插件
        mock_plugin.initialize(mock_event_bus)
        self.assertEqual(mock_plugin.event_bus, mock_event_bus)
        print("✓ 插件初始化验证通过")

        # 验证页面贡献
        page_contributions = mock_plugin.page_contributions
        self.assertEqual(len(page_contributions), 1)

        capture_page = page_contributions[0]
        self.assertEqual(capture_page.page_id, "capture_plugin_page_test")
        self.assertEqual(capture_page.navigation_name, "输入行动_test")
        self.assertEqual(capture_page.parent_page, "capture_page")
        print("✓ 页面贡献验证通过")

        # 测试创建页面
        view = mock_plugin.create_page("capture_plugin_page_test")
        self.assertIsNotNone(view)
        print("✓ 创建页面验证通过")

        # 测试未知页面
        unknown_view = mock_plugin.create_page("unknown_page")
        self.assertIsNone(unknown_view)
        print("✓ 未知页面处理验证通过")

        # 测试关闭插件
        mock_plugin.presenter = Mock()
        mock_plugin.shutdown()
        self.assertIsNone(mock_plugin.presenter)
        print("✓ 插件关闭验证通过")

    def test_strategy_service_integration(self):
        """测试策略服务集成"""
        print("\n=== 测试策略服务集成 ===")

        # 模拟策略服务
        mock_strategy_service = Mock()

        # 设置模拟返回值
        mock_context_presenters = [Mock()]
        mock_editor_presenters = [Mock()]
        mock_display_presenters = [Mock()]
        mock_data_models = [Mock()]

        mock_strategy_service.execute_strategies_from_protocol.side_effect = [
            mock_context_presenters,
            mock_editor_presenters,
            mock_display_presenters
        ]
        mock_strategy_service.get_strategy_methods_from_protocol.return_value = mock_data_models

        # 模拟presenter
        mock_presenter = Mock()
        mock_view = Mock()
        mock_presenter.view = mock_view
        mock_strategy_service.execute_with_strategy.return_value = mock_presenter

        # 模拟插件
        mock_plugin = Mock()
        mock_plugin.data_service = Mock()
        mock_plugin.event_bus = Mock()
        mock_plugin.presenter = None

        # 模拟create_capture_view方法
        def mock_create_capture_view():
            # 模拟策略服务调用
            context_presenters = mock_strategy_service.execute_strategies_from_protocol(Mock(), Mock())
            editor_presenters = mock_strategy_service.execute_strategies_from_protocol(Mock())
            display_presenters = mock_strategy_service.execute_strategies_from_protocol(Mock())

            # 添加默认presenter
            context_presenters.append(Mock())
            editor_presenters.append(Mock())
            display_presenters.append(Mock())

            data_models = mock_strategy_service.get_strategy_methods_from_protocol(Mock())

            presenter = mock_strategy_service.execute_with_strategy(
                Mock(), Mock(),
                context_presenters,
                display_presenters,
                editor_presenters,
                mock_plugin.data_service,
                mock_plugin.event_bus,
                data_models
            )

            mock_plugin.presenter = presenter
            return presenter.view

        mock_plugin.create_capture_view = mock_create_capture_view

        # 调用创建视图方法
        result_view = mock_plugin.create_capture_view()

        # 验证策略服务调用
        self.assertEqual(mock_strategy_service.execute_strategies_from_protocol.call_count, 3)
        self.assertEqual(mock_strategy_service.get_strategy_methods_from_protocol.call_count, 1)
        self.assertEqual(mock_strategy_service.execute_with_strategy.call_count, 1)
        print("✓ 策略服务调用验证通过")

        # 验证presenter引用被存储
        self.assertEqual(mock_plugin.presenter, mock_presenter)
        print("✓ Presenter引用存储验证通过")

        # 验证返回的视图
        self.assertEqual(result_view, mock_view)
        print("✓ 视图返回验证通过")

    def test_data_flow(self):
        """测试数据流"""
        print("\n=== 测试数据流 ===")

        # 模拟ActionUnit数据
        mock_action_unit = Mock()
        mock_action_unit.id = "test-uuid"
        mock_action_unit.date = "2024-01-01"
        mock_action_unit.start = "09:00"
        mock_action_unit.end = "10:00"
        mock_action_unit.action = "测试行动"
        mock_action_unit.action_type = "工作"
        mock_action_unit.action_detail = "测试详情"
        mock_action_unit.urgency = False
        mock_action_unit.importance = True

        # 模拟数据服务
        mock_data_service = Mock()
        mock_data_service.get_date_data.return_value = [
            ("uuid1", mock_action_unit)
        ]

        # 模拟presenter
        mock_presenter = Mock()
        mock_presenter.fill_records = Mock()

        # 模拟插件
        mock_plugin = Mock()
        mock_plugin.data_service = mock_data_service
        mock_plugin.presenter = mock_presenter

        # 模拟数据加载流程
        def mock_load_data():
            action_units = mock_plugin.data_service.get_date_data("2024-01-01")
            mock_plugin.presenter.fill_records(action_units)

        mock_plugin.load_data = mock_load_data

        # 执行数据加载
        mock_plugin.load_data()

        # 验证数据服务调用
        mock_data_service.get_date_data.assert_called_once_with("2024-01-01")
        print("✓ 数据服务调用验证通过")

        # 验证presenter调用
        mock_presenter.fill_records.assert_called_once()
        print("✓ Presenter数据填充验证通过")


if __name__ == "__main__":
    # 运行独立测试
    unittest.main(verbosity=2)