"""
验收测试：干预插件 (Intervention Plugin)

这个测试验证干预插件的主要功能，包括：
1. 插件初始化
2. 项目创建和配置
3. 事件源和视图的集成
4. 用户交互流程
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from PyQt6.QtWidgets import QApplication
import sys

from ti.features.intervention.interventionPlugin import InterventionPlugin
from ti.core.eventBus import EventBus
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.function_service import FunctionService
from ti.services.symbol_service import SymbolService
from ti.model.yaml_repository import YamlRepository
from ti.features.intervention.intervention_path_register import INV_PathRegister


class TestInterventionPluginAcceptance:
    """干预插件验收测试"""
    
    def setup_method(self):
        """测试方法前的设置"""
        # 创建模拟的服务对象
        self.mock_bus = Mock(spec=EventBus)
        self.mock_monitor = Mock(spec=RealTimeMonitor)
        self.mock_function_service = Mock(spec=FunctionService)
        self.mock_symbol_service = Mock(spec=SymbolService)
        
        # 模拟detector factory函数
        self.mock_detector_factory = Mock()
        self.mock_function_service.get_function.return_value = self.mock_detector_factory
        
        # 设置Qt应用（如果需要UI测试）
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
    
    def test_plugin_initialization(self):
        """测试插件初始化过程"""
        # 模拟YAML仓库返回配置数据
        mock_project_repository = Mock(spec=YamlRepository)
        mock_project_recipe_repository = Mock(spec=YamlRepository)
        
        # 模拟配置数据 - 使用现有的post_eat_waste项目配置
        mock_project_data = {
            "post_eat_waste": {
                "project_id": "post_eat_waste",
                "eventSources": {},
                "views": []
            }
        }
        mock_project_repository.get_all.return_value = mock_project_data
        
        mock_recipe_data = {
            "post_eat_waste": {
                "event_sources": {
                    "class_name": "intervention.ACTION_EVENT_SOURCE",
                    "rule": {
                        "detector_id": "post_eat_waste",
                        "event_source_id": "post_eat_waste_source"
                    }
                },
                "views": [
                    {
                        "post_eat_waste_view": {
                            "view_id": "post_eat_waste_view",
                            "state": {
                                "init": {
                                    "name": "init",
                                    "transition": {
                                        "user_accepted": "intervene_user",
                                        "user_rejected": "intervene_user"
                                    },
                                    "presentation": {
                                        "button": {
                                            "接受": "user_accepted",
                                            "拒绝": "user_rejected"
                                        },
                                        "title": "我要打荒野乱斗"
                                    },
                                    "entering_event": None
                                }
                            },
                            "initial_state": "init"
                        }
                    }
                ],
                "project_id": "post_eat_waste"
            }
        }
        mock_project_recipe_repository.get_all.return_value = mock_recipe_data
        
        # 模拟YamlRepository构造函数
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.side_effect = [mock_project_repository, mock_project_recipe_repository]
            
            # 创建插件实例
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 验证插件属性
        assert plugin.name == "Intervention"
        
        # 验证服务调用
        self.mock_function_service.get_function.assert_called_once_with("get_detector_factory")
        
        # 验证YAML仓库创建
        assert mock_yaml_repo.call_count == 2
        mock_yaml_repo.assert_any_call("ti/features/refactored_intervention/model/inv_projects.yaml")
        mock_yaml_repo.assert_any_call("ti/features/refactored_intervention/model/inv_project_recipe.yaml")
    
    def test_plugin_interface_methods(self):
        """测试插件接口方法"""
        # 创建插件实例
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.return_value = Mock(spec=YamlRepository)
            
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 测试name属性
        assert plugin.name == "Intervention"
        
        # 测试initialize方法
        plugin.initialize(self.mock_bus)
        # initialize方法应该不抛出异常
        
        # 测试shutdown方法
        result = plugin.shutdown()
        assert result is None
        
        # 测试register_class方法
        register_class = plugin.register_class()
        assert register_class == INV_PathRegister
    
    def test_plugin_with_empty_configuration(self):
        """测试插件处理空配置的情况"""
        # 模拟空的YAML仓库
        mock_project_repository = Mock(spec=YamlRepository)
        mock_project_recipe_repository = Mock(spec=YamlRepository)
        
        mock_project_repository.get_all.return_value = {}
        mock_project_recipe_repository.get_all.return_value = {}
        
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.side_effect = [mock_project_repository, mock_project_recipe_repository]
            
            # 创建插件实例
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 验证插件正常创建
        assert plugin.name == "Intervention"
        
        # 验证仓库方法被调用
        mock_project_repository.get_all.assert_called_once()
        mock_project_recipe_repository.get_all.assert_called_once()
    
    def test_plugin_with_invalid_detector_factory(self):
        """测试插件处理无效detector factory的情况"""
        # 模拟无效的detector factory
        self.mock_function_service.get_function.return_value = None
        
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.return_value = Mock(spec=YamlRepository)
            
            # 插件应该能够处理这种情况
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 验证插件正常创建
        assert plugin.name == "Intervention"
        
        # 验证函数服务被调用
        self.mock_function_service.get_function.assert_called_once_with("get_detector_factory")
    
    def test_plugin_integration_with_real_config(self):
        """测试插件与真实配置的集成"""
        # 模拟真实的配置数据
        mock_project_repository = Mock(spec=YamlRepository)
        mock_project_recipe_repository = Mock(spec=YamlRepository)
        
        # 使用现有的post_eat_waste项目配置
        real_project_data = {
            "post_eat_waste": {
                "project_id": "post_eat_waste",
                "eventSources": {},
                "views": []
            }
        }
        
        real_recipe_data = {
            "post_eat_waste": {
                "event_sources": {
                    "class_name": "ti.features.refactored_intervention.service.inv_action_event_source.INVActionEventSource",
                    "rule": {
                        "detector_id": "post_eat_waste",
                        "event_source_id": "post_eat_waste_source"
                    }
                },
                "views": [
                    {
                        "class_name": "ti.features.intervention.view.interventionCard.InterventionCard",
                        "rule": {
                            "view_id": "post_eat_waste_view",
                            "states": {
                                "init": {
                                    "name": "init",
                                    "transitions": {
                                        "user_accepted": "intervene_user",
                                        "user_rejected": "intervene_user"
                                    },
                                    "presentation": {
                                        "buttons": {
                                            "接受": "user_accepted",
                                            "拒绝": "user_rejected"
                                        },
                                        "title": "我要打荒野乱斗"
                                    }
                                }
                            },
                            "initial_state": "init"
                        }
                    }
                ],
                "project_id": "post_eat_waste"
            }
        }
        
        mock_project_repository.get_all.return_value = real_project_data
        mock_project_recipe_repository.get_all.return_value = real_recipe_data
        
        # 模拟SymbolService返回真实的类
        from ti.features.intervention.service.inv_action_event_source import INVActionEventSource
        from ti.features.intervention.view.interventionCard import InterventionCard
        
        self.mock_symbol_service.get_symbol.side_effect = [INVActionEventSource, InterventionCard]
        
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.side_effect = [mock_project_repository, mock_project_recipe_repository]
            
            # 创建插件实例
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 验证插件正常创建
        assert plugin.name == "Intervention"
        
        # 验证配置数据被正确使用
        mock_project_repository.get_all.assert_called_once()
        mock_project_recipe_repository.get_all.assert_called_once()
    
    def test_plugin_error_handling(self):
        """测试插件的错误处理能力"""
        # 模拟YAML仓库抛出异常
        mock_project_repository = Mock(spec=YamlRepository)
        mock_project_recipe_repository = Mock(spec=YamlRepository)
        
        mock_project_repository.get_all.side_effect = Exception("File not found")
        mock_project_recipe_repository.get_all.side_effect = Exception("File not found")
        
        with patch('ti.features.intervention.interventionPlugin.YamlRepository') as mock_yaml_repo:
            mock_yaml_repo.side_effect = [mock_project_repository, mock_project_recipe_repository]
            
            # 插件应该能够处理异常情况
            plugin = InterventionPlugin(
                self.mock_bus,
                self.mock_monitor,
                self.mock_function_service,
                self.mock_symbol_service
            )
        
        # 验证插件正常创建
        assert plugin.name == "Intervention"
        
        # 验证异常被捕获和处理
        mock_project_repository.get_all.assert_called_once()
        mock_project_recipe_repository.get_all.assert_called_once()


class TestInterventionPluginPathRegister:
    """测试干预插件的路径注册功能"""
    
    def test_path_register_creation(self):
        """测试路径注册器的创建"""
        path_register = INV_PathRegister()
        
        # 验证路径注册器包含必要的路径
        assert hasattr(path_register, 'paths')
        assert isinstance(path_register.paths, list)
        
        # 验证包含干预相关的路径
        intervention_paths = [path for path in path_register.paths if 'intervention' in path]
        assert len(intervention_paths) > 0
    
    def test_path_register_content(self):
        """测试路径注册器的具体内容"""
        path_register = INV_PathRegister()
        
        # 验证包含关键路径
        expected_paths = [
            'ti/features/intervention',
            'ti/features/refactored_intervention'
        ]
        
        for expected_path in expected_paths:
            assert any(expected_path in path for path in path_register.paths)


if __name__ == "__main__":
    # 运行验收测试
    pytest.main([__file__, "-v"])