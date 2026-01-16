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
            def __init__(self, recipe, bus, project_id, view_id):
                self.recipe = recipe
                self.bus = bus
                self.project_id = project_id
                self.view_id = view_id
        
        # 模拟resolve_component_class方法
        def mock_resolve(class_path, default_domain):
            if "action_event_source" in class_path:
                return MockEventSource
            elif "card_view" in class_path:
                return MockViewClass
            else:
                # 模拟规则类
                class MockRuleClass:
                    def __init__(self, **kwargs):
                        for k, v in kwargs.items():
                            setattr(self, k, v)
                return MockRuleClass
        
        self.mock_symbol_service.resolve_component_class.side_effect = mock_resolve
        
        # 执行测试
        result = self.factory.create_projects()
        
        # 验证结果
        assert isinstance(result, dict)
        assert "test_project" in result
        assert isinstance(result["test_project"], INVProjects)
        assert result["test_project"].project_id == "test_project"
        
        # 验证方法调用
        self.mock_recipe_repository.get_all.assert_called_once()
        # 验证resolve_component_class被调用（至少两次：一次用于事件源，一次用于视图）
        assert self.mock_symbol_service.resolve_component_class.call_count >= 2
    
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
        
        # 模拟resolve_component_class方法
        def mock_resolve(class_path, default_domain):
            if "action_event_source" in class_path:
                return MockEventSource
            else:
                # 模拟规则类
                class MockRuleClass:
                    def __init__(self, **kwargs):
                        for k, v in kwargs.items():
                            setattr(self, k, v)
                return MockRuleClass
        
        self.mock_symbol_service.resolve_component_class.side_effect = mock_resolve
        
        # 执行测试
        result = self.factory._create_event_sources(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "source1" in result
        assert isinstance(result["source1"], MockEventSource)
        
        # 验证方法调用
        assert self.mock_symbol_service.resolve_component_class.call_count == 2
        # 第一次调用：解析事件源类
        self.mock_symbol_service.resolve_component_class.assert_any_call(
            "intervention.action_event_source", "intervention"
        )
        # 第二次调用：解析规则类
        self.mock_symbol_service.resolve_component_class.assert_any_call(
            "ti.features.intervention.model.stored.inv_component_rule.ActionEventSourceRule", "intervention"
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
        
        self.mock_symbol_service.resolve_component_class.return_value = InvalidClass
        
        # 执行测试
        result = self.factory._create_event_sources(project_recipe)
        
        # 验证结果（无效类应该被跳过）
        assert isinstance(result, dict)
        assert len(result) == 0
        
        # 验证方法调用
        self.mock_symbol_service.resolve_component_class.assert_called_once_with("invalid.InvalidClass", "intervention")
    
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
            def __init__(self, recipe, bus, project_id, view_id):
                self.recipe = recipe
                self.bus = bus
                self.project_id = project_id
                self.view_id = view_id
        
        # 模拟resolve_component_class方法
        def mock_resolve(class_path, default_domain):
            if "card_view" in class_path:
                return MockViewClass
            else:
                # 模拟规则类
                class MockRuleClass:
                    def __init__(self, **kwargs):
                        for k, v in kwargs.items():
                            setattr(self, k, v)
                return MockRuleClass
        
        self.mock_symbol_service.resolve_component_class.side_effect = mock_resolve
        
        # 执行测试
        result = self.factory._create_views(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "view1" in result  # 现在使用字典键而不是view_id
        assert isinstance(result["view1"], MockViewClass)
        # 现在规则是解析后的对象，不再是INVComponentRule
        assert hasattr(result["view1"].recipe, 'view_id')
        
        # 验证方法调用
        assert self.mock_symbol_service.resolve_component_class.call_count == 2
        # 第一次调用：解析视图类
        self.mock_symbol_service.resolve_component_class.assert_any_call(
            "intervention.card_view", "intervention"
        )
        # 第二次调用：解析规则类
        self.mock_symbol_service.resolve_component_class.assert_any_call(
            "ti.features.intervention.model.stored.inv_view_state.INVViewRecipe", "intervention"
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
            def __init__(self, recipe, bus, project_id, view_id):
                self.recipe = recipe
                self.bus = bus
                self.project_id = project_id
                self.view_id = view_id
        
        # 模拟resolve_component_class方法
        def mock_resolve(class_path, default_domain):
            if "card_view" in class_path:
                return MockViewClass
            else:
                # 模拟规则类
                class MockRuleClass:
                    def __init__(self, **kwargs):
                        for k, v in kwargs.items():
                            setattr(self, k, v)
                return MockRuleClass
        
        self.mock_symbol_service.resolve_component_class.side_effect = mock_resolve
        
        # 执行测试
        result = self.factory._create_views(project_recipe)
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "view1" in result
        assert "view2" in result
        
        # 验证方法调用次数（每个视图调用2次：视图类 + 规则类）
        assert self.mock_symbol_service.resolve_component_class.call_count == 4
    
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
        self.mock_symbol_service.resolve_component_class.side_effect = ImportError("Module not found")
        
        # 执行测试（异常应该传播）
        with pytest.raises(ImportError, match="Module not found"):
            self.factory._create_event_sources(project_recipe)
        
        # 验证方法调用
        self.mock_symbol_service.resolve_component_class.assert_called_once_with("invalid.NonExistentClass", "intervention")
    
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