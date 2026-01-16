import pytest
from unittest.mock import Mock, MagicMock
from ti.services.symbol_service import SymbolService
from ti.model.symbol_models import SymbolModel, SymbolType


class TestSymbolService:
    
    def test_regist_register(self):
        """测试注册register功能"""
        service = SymbolService()
        mock_register = Mock()
        mock_register.domain = "test_domain"
        
        service.regist_register(mock_register)
        
        assert "test_domain" in service.registers
        assert service.registers["test_domain"] == mock_register
    
    def test_find_symbol_success(self):
        """测试成功查找符号路径"""
        service = SymbolService()
        mock_register = Mock()
        mock_register.domain = "test_domain"
        
        # 创建模拟的symbol model
        mock_symbol_model = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TestClass",
            symbol_domain="test_domain"
        )
        
        mock_register.get_symbol_path.return_value = mock_symbol_model
        service.registers["test_domain"] = mock_register
        
        result = service.find_symbol("test_domain", "TestClass")
        
        assert result == "ti.test.module.TestClass"
        mock_register.get_symbol_path.assert_called_once_with("TestClass")
    
    def test_find_symbol_not_found(self):
        """测试查找不存在的符号"""
        service = SymbolService()
        mock_register = Mock()
        mock_register.domain = "test_domain"
        mock_register.get_symbol_path.return_value = None
        
        service.registers["test_domain"] = mock_register
        
        result = service.find_symbol("test_domain", "NonExistentClass")
        
        assert result is None
        mock_register.get_symbol_path.assert_called_once_with("NonExistentClass")
    
    def test_find_symbol_domain_not_registered(self):
        """测试查找未注册的domain"""
        service = SymbolService()
        
        with pytest.raises(ValueError, match="Domain 'unknown_domain' not registered"):
            service.find_symbol("unknown_domain", "TestClass")
    
    def test_get_symbol_success(self, mocker):
        """测试成功获取符号对象"""
        service = SymbolService()
        
        # 模拟一个测试类
        class TestClass:
            test_attr = "test_value"
        
        # 模拟import_module和getattr
        mock_module = Mock()
        mock_module.TestClass = TestClass
        
        mock_import = mocker.patch('importlib.import_module')
        mock_import.return_value = mock_module
        
        result = service.get_symbol("ti.test.module.TestClass")
        
        assert result == TestClass
        mock_import.assert_called_once_with("ti.test.module")
    
    def test_get_symbol_module_not_found(self, mocker):
        """测试模块不存在的情况"""
        service = SymbolService()
        
        mock_import = mocker.patch('importlib.import_module')
        mock_import.side_effect = ImportError("Module not found")
        
        with pytest.raises(ImportError, match="Could not import module 'nonexistent.module': Module not found"):
            service.get_symbol("nonexistent.module.TestClass")
    
    def test_get_symbol_symbol_not_found(self, mocker):
        """测试符号不存在的情况"""
        service = SymbolService()
        
        # 模拟import_module返回一个Mock模块
        mock_import = mocker.patch('importlib.import_module')
        
        # 创建一个特殊的Mock对象，当访问TestClass属性时抛出AttributeError
        class MockModuleWithMissingAttribute:
            def __init__(self):
                pass
            
            def __getattr__(self, name):
                if name == 'TestClass':
                    raise AttributeError("module 'ti.test.module' has no attribute 'TestClass'")
                return Mock()
        
        mock_module = MockModuleWithMissingAttribute()
        mock_import.return_value = mock_module
        
        with pytest.raises(AttributeError, match="Symbol 'TestClass' not found in module 'ti.test.module':"):
            service.get_symbol("ti.test.module.TestClass")
    
    def test_get_symbol_empty_path(self):
        """测试空路径的情况"""
        service = SymbolService()
        
        with pytest.raises(ValueError, match="Symbol path cannot be empty"):
            service.get_symbol("")
    
    def test_get_symbol_invalid_format(self):
        """测试无效路径格式的情况"""
        service = SymbolService()
        
        with pytest.raises(ValueError, match="Invalid symbol path format: TestClass"):
            service.get_symbol("TestClass")
    
    def test_resolve_symbol_success(self, mocker):
        """测试成功解析符号"""
        service = SymbolService()
        
        # 模拟find_symbol返回路径
        mock_find = mocker.patch.object(service, 'find_symbol')
        mock_find.return_value = "ti.test.module.TestClass"
        
        # 模拟get_symbol返回对象
        class TestClass:
            pass
        
        mock_get = mocker.patch.object(service, 'get_symbol')
        mock_get.return_value = TestClass
        
        result = service.resolve_symbol("test_domain", "TestClass")
        
        assert result == TestClass
        mock_find.assert_called_once_with("test_domain", "TestClass")
        mock_get.assert_called_once_with("ti.test.module.TestClass")
    
    def test_resolve_symbol_not_found(self, mocker):
        """测试解析不存在的符号"""
        service = SymbolService()
        
        mock_find = mocker.patch.object(service, 'find_symbol')
        mock_find.return_value = None
        
        with pytest.raises(ValueError, match="Symbol 'NonExistentClass' not found in domain 'test_domain'"):
            service.resolve_symbol("test_domain", "NonExistentClass")
        
        mock_find.assert_called_once_with("test_domain", "NonExistentClass")
    
    def test_integration_flow(self, mocker):
        """测试完整的集成流程"""
        service = SymbolService()
        
        # 模拟register
        mock_register = Mock()
        mock_register.domain = "test_domain"
        
        # 模拟symbol model
        mock_symbol_model = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TestClass",
            symbol_domain="test_domain"
        )
        mock_register.get_symbol_path.return_value = mock_symbol_model
        
        service.regist_register(mock_register)
        
        # 模拟模块导入
        class TestClass:
            test_value = "success"
        
        mock_module = Mock()
        mock_module.TestClass = TestClass
        
        mock_import = mocker.patch('importlib.import_module')
        mock_import.return_value = mock_module
        
        # 执行完整的解析流程
        result = service.resolve_symbol("test_domain", "TestClass")
        
        assert result == TestClass
        assert result.test_value == "success"
        
        # 验证调用链
        mock_register.get_symbol_path.assert_called_once_with("TestClass")
        mock_import.assert_called_once_with("ti.test.module")