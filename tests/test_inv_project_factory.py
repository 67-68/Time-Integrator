import pytest
from unittest.mock import Mock, MagicMock
from ti.features.intervention.service.inv_project_factory import INVProjectFactory
from ti.features.intervention.model.stored.inv_project_recipe import INVProjectRecipe, INVComponentRecipe, INVProjects
from ti.features.intervention.model.stored.inv_component_rule import ActionEventSourceRule, INVComponentRule
from ti.features.intervention.service.inv_action_event_source import INVActionEventSource


class TestINVProjectFactory:
    
    def setup_method(self):
        """设置测试环境"""
        # 创建模拟的依赖对象
        self.mock_bus = Mock()
        self.mock_monitor = Mock()
        self.mock_detector_repository = Mock()
        self.mock_symbol_service = Mock()
        self.mock_recipe_repository = Mock()
        
        # 创建工厂实例
        self.factory = INVProjectFactory(
            bus=self.mock_bus,
            monitor=self.mock_monitor,
            detector_repository=self.mock_detector_repository,
            symbol_service=self.mock_symbol_service,
            recipe_repository=self.mock_recipe_repository
        )
    
    def test_create_projects_with_valid_recipes(self):
        """测试使用有效配方创建项目"""
        # 创建模拟的配方数据
        event_source_recipe = INVComponentRecipe(
            class_name="intervention.action_event_source",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_component_rule.ActionEventSourceRule",
                "data": {
                    "event_source_id": "test_event_source",
                    "detector_id": "test_detector"
                }
            }
        )
        
        view_recipe = INVComponentRecipe(
            class_name="intervention.card_view",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_view_state.INVViewRecipe",
                "data": {
                    "view_id": "test_view",
                    "state": {},
                    "initial_state": "init"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={"source1": event_source_recipe},
            views={"view1": view_recipe},
            project_id="test_project"
        )
        
        # 模拟配方仓库返回数据
        self.mock_recipe_repository.get_all.return_value = [project_recipe]
        
        # 模拟符号服务返回类
        # 创建一个模拟的INVActionEventSource子类
        class MockEventSource(INVActionEventSource):
            def __init__(self, repo, monitor):
                super().__init__(repo, monitor)
            
            def initialize(self, project_id, bus, rule):
                pass
        
        # 模拟视图类
        class MockViewClass:
            def __init__(self, rule):
                self.rule = rule
        
        # 模拟resolve_symbol方法
        self.mock_symbol_service.resolve_symbol.side_effect = lambda domain, symbol_name: MockEventSource if symbol_name == "action_event_source" else MockViewClass
        
        # 执行测试
        result = self.factory.create_projects()
        
        # 验证结果
        assert isinstance(result, dict)
        assert "test_project" in result
        assert isinstance(result["test_project"], INVProjects)
        assert result["test_project"].project_id == "test_project"
        
        # 验证方法调用
        self.mock_recipe_repository.get_all.assert_called_once()
        # 验证resolve_symbol被调用（至少两次：一次用于事件源，一次用于视图）
        assert self.mock_symbol_service.resolve_symbol.call_count >= 2
    
    def test_create_projects_with_empty_recipes(self):
        """测试使用空配方创建项目"""
        # 模拟空配方列表
        self.mock_recipe_repository.get_all.return_value = []
        
        # 执行测试
        result = self.factory.create_projects()
        
        # 验证结果
        assert result is None
        self.mock_recipe_repository.get_all.assert_called_once()
    
    def test_create_event_sources_success(self):
        """测试成功创建事件源"""
        # 创建模拟配方
        event_source_recipe = INVComponentRecipe(
            class_name="intervention.action_event_source",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_component_rule.ActionEventSourceRule",
                "data": {
                    "event_source_id": "test_event_source",
                    "detector_id": "test_detector"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={"source1": event_source_recipe},
            views={},
            project_id="test_project"
        )
        
        # 模拟符号服务返回INVActionEventSource类
        # 创建一个模拟的INVActionEventSource子类
        class MockEventSource(INVActionEventSource):
            def __init__(self, repo, monitor):
                super().__init__(repo, monitor)
            
            def initialize(self, project_id, bus, rule):
                pass
        
        # 模拟resolve_symbol方法
        self.mock_symbol_service.resolve_symbol.return_value = MockEventSource
        
        # 执行测试
        result = self.factory._create_event_sources(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "source1" in result
        assert isinstance(result["source1"], MockEventSource)
        
        # 验证方法调用
        self.mock_symbol_service.resolve_symbol.assert_called_once_with(
            "intervention", "action_event_source"
        )
    
    def test_create_event_sources_invalid_class(self):
        """测试创建无效类的事件源"""
        # 创建模拟配方（使用无效类）
        event_source_recipe = INVComponentRecipe(
            class_name="invalid.InvalidClass",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_component_rule.ActionEventSourceRule",
                "data": {
                    "event_source_id": "test_event_source",
                    "detector_id": "test_detector"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={"source1": event_source_recipe},
            views={},
            project_id="test_project"
        )
        
        # 模拟符号服务返回非INVActionEventSource类
        class InvalidClass:
            pass
        
        self.mock_symbol_service.resolve_symbol.return_value = InvalidClass
        
        # 执行测试
        result = self.factory._create_event_sources(project_recipe)
        
        # 验证结果（无效类应该被跳过）
        assert isinstance(result, dict)
        assert len(result) == 0
        
        # 验证方法调用
        self.mock_symbol_service.resolve_symbol.assert_called_once_with("invalid", "InvalidClass")
    
    def test_create_views_success(self):
        """测试成功创建视图"""
        # 创建模拟配方
        view_recipe = INVComponentRecipe(
            class_name="intervention.card_view",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_view_state.INVViewRecipe",
                "data": {
                    "view_id": "test_view",
                    "state": {},
                    "initial_state": "init"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={},
            views={"view1": view_recipe},
            project_id="test_project"
        )
        
        # 模拟视图类
        class MockViewClass:
            def __init__(self, rule):
                self.rule = rule
        
        self.mock_symbol_service.resolve_symbol.return_value = MockViewClass
        
        # 执行测试
        result = self.factory._create_views(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "view1" in result  # 现在使用字典键而不是view_id
        assert isinstance(result["view1"], MockViewClass)
        # 现在规则是解析后的对象，不再是INVComponentRule
        assert hasattr(result["view1"].rule, 'view_id')
        
        # 验证方法调用
        self.mock_symbol_service.resolve_symbol.assert_called_once_with(
            "intervention", "card_view"
        )
    
    def test_create_views_multiple(self):
        """测试创建多个视图"""
        # 创建多个模拟配方
        view_recipe1 = INVComponentRecipe(
            class_name="intervention.card_view",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_view_state.INVViewRecipe",
                "data": {
                    "view_id": "test_view1",
                    "state": {},
                    "initial_state": "init"
                }
            }
        )
        
        view_recipe2 = INVComponentRecipe(
            class_name="intervention.card_view",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_view_state.INVViewRecipe",
                "data": {
                    "view_id": "test_view2",
                    "state": {},
                    "initial_state": "init"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={},
            views={"view1": view_recipe1, "view2": view_recipe2},
            project_id="test_project"
        )
        
        # 模拟视图类
        class MockViewClass:
            def __init__(self, rule):
                self.rule = rule
        
        self.mock_symbol_service.resolve_symbol.return_value = MockViewClass
        
        # 执行测试
        result = self.factory._create_views(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "view1" in result
        assert "view2" in result
        
        # 验证方法调用次数
        assert self.mock_symbol_service.resolve_symbol.call_count == 2
    
    def test_integration_multiple_projects(self):
        """测试集成场景：创建多个项目"""
        # 创建多个项目配方
        project_recipe1 = INVProjectRecipe(
            event_sources={},
            views={},
            project_id="project1"
        )
        
        project_recipe2 = INVProjectRecipe(
            event_sources={},
            views={},
            project_id="project2"
        )
        
        # 模拟配方仓库返回多个配方
        self.mock_recipe_repository.get_all.return_value = [project_recipe1, project_recipe2]
        
        # 执行测试
        result = self.factory.create_projects()
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "project1" in result
        assert "project2" in result
        assert isinstance(result["project1"], INVProjects)
        assert isinstance(result["project2"], INVProjects)
    
    def test_symbol_service_error_handling(self):
        """测试符号服务错误处理"""
        # 创建模拟配方
        event_source_recipe = INVComponentRecipe(
            class_name="invalid.NonExistentClass",
            rule={
                "rule_type": "ti.features.intervention.model.stored.inv_component_rule.ActionEventSourceRule",
                "data": {
                    "event_source_id": "test_event_source",
                    "detector_id": "test_detector"
                }
            }
        )
        
        project_recipe = INVProjectRecipe(
            event_sources={"source1": event_source_recipe},
            views={},
            project_id="test_project"
        )
        
        # 模拟符号服务抛出异常
        self.mock_symbol_service.resolve_symbol.side_effect = ImportError("Module not found")
        
        # 执行测试（异常应该传播）
        with pytest.raises(ImportError, match="Module not found"):
            self.factory._create_event_sources(project_recipe)
        
        # 验证方法调用
        self.mock_symbol_service.resolve_symbol.assert_called_once_with("invalid", "NonExistentClass")
    
    def test_recipe_repository_error_handling(self):
        """测试配方仓库错误处理"""
        # 模拟配方仓库抛出异常
        self.mock_recipe_repository.get_all.side_effect = Exception("Database error")
        
        # 执行测试并验证异常传播
        with pytest.raises(Exception, match="Database error"):
            self.factory.create_projects()
        
        # 验证方法调用
        self.mock_recipe_repository.get_all.assert_called_once()


class TestINVProjectFactoryEdgeCases:
    """测试边界情况"""
    
    def test_create_projects_with_none_recipe(self):
        """测试配方为None的情况"""
        factory = INVProjectFactory(
            bus=Mock(),
            monitor=Mock(),
            detector_repository=Mock(),
            symbol_service=Mock(),
            recipe_repository=Mock()
        )
        
        # 模拟配方仓库返回None
        factory.recipe_repository.get_all.return_value = None
        
        # 执行测试
        result = factory.create_projects()
        
        # 验证结果
        assert result is None
    
    def test_create_event_sources_empty_recipe(self):
        """测试空配方的事件源创建"""
        factory = INVProjectFactory(
            bus=Mock(),
            monitor=Mock(),
            detector_repository=Mock(),
            symbol_service=Mock(),
            recipe_repository=Mock()
        )
        
        # 创建空事件源的配方
        project_recipe = INVProjectRecipe(
            event_sources={},
            views={},
            project_id="test_project"
        )
        
        # 执行测试
        result = factory._create_event_sources(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_create_views_empty_recipe(self):
        """测试空配方的视图创建"""
        factory = INVProjectFactory(
            bus=Mock(),
            monitor=Mock(),
            detector_repository=Mock(),
            symbol_service=Mock(),
            recipe_repository=Mock()
        )
        
        # 创建空视图的配方
        project_recipe = INVProjectRecipe(
            event_sources={},
            views={},
            project_id="test_project"
        )
        
        # 执行测试
        result = factory._create_views(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) == 0