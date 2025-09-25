import pytest
from unittest.mock import Mock, patch, mock_open
from ti.features.detector.detector_path_register import DetectorPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml


class TestDetectorPathRegister:
    
    def test_domain_property(self):
        """测试domain属性"""
        register = DetectorPathRegister()
        assert register.domain == "detector"
    
    def test_file_path_properties(self):
        """测试文件路径属性"""
        register = DetectorPathRegister()
        
        assert register.class_file_path == "ti/features/detector/model/data/detector_classes.yaml"
        assert register.class_method_file_path == "ti/features/detector/model/data/detector_class_methods.yaml"
        assert register.function_file_path == "ti/features/detector/model/data/detector_functions.yaml"
        assert register.enum_file_path == "ti/features/detector/model/data/detector_enums.yaml"
    
    def test_regist_symbol_path(self):
        """测试注册符号路径"""
        register = DetectorPathRegister()
        
        # 清空现有符号以便测试
        register._symbols = {}
        
        symbol_model = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TestClass",
            symbol_domain="detector"
        )
        
        register.regist_symbol_path(symbol_model)
        
        expected_id = "class:ti.test.module.TestClass"
        assert expected_id in register._symbols
        assert register._symbols[expected_id] == symbol_model
    
    def test_get_symbol_path_found(self):
        """测试获取已存在的符号路径"""
        register = DetectorPathRegister()
        
        # 清空现有符号并添加测试符号
        register._symbols = {}
        
        symbol_model = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TestClass",
            symbol_domain="detector"
        )
        register.regist_symbol_path(symbol_model)
        
        # 根据实现，应该使用symbol_path来查找，而不是完整的symbol_id
        result = register.get_symbol_path("ti.test.module.TestClass")
        assert result == symbol_model
    
    def test_get_symbol_path_not_found(self):
        """测试获取不存在的符号路径"""
        register = DetectorPathRegister()
        
        # 清空现有符号
        register._symbols = {}
        
        result = register.get_symbol_path("class:nonexistent.Class")
        assert result is None
    
    def test_search_symbol_data_by_type(self):
        """测试按类型搜索符号"""
        register = DetectorPathRegister()
        
        # 清空现有符号并添加测试数据
        register._symbols = {}
        
        # 添加不同类型的符号
        class_symbol = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TestClass",
            symbol_domain="detector"
        )
        function_symbol = SymbolModel(
            symbol_type=SymbolType.FUNCTION,
            symbol_path="ti.test.module.test_function",
            symbol_domain="detector"
        )
        
        register.regist_symbol_path(class_symbol)
        register.regist_symbol_path(function_symbol)
        
        # 搜索类符号
        class_results = register.search_symbol_data(symbol_type=SymbolType.CLASS)
        assert len(class_results) == 1
        assert class_results[0] == class_symbol
        
        # 搜索函数符号
        function_results = register.search_symbol_data(symbol_type=SymbolType.FUNCTION)
        assert len(function_results) == 1
        assert function_results[0] == function_symbol
    
    def test_search_symbol_data_by_domain(self):
        """测试按域名搜索符号"""
        register = DetectorPathRegister()
        
        # 清空现有符号并添加测试数据
        register._symbols = {}
        
        # 添加不同域的符号
        detector_symbol = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.DetectorClass",
            symbol_domain="detector"
        )
        other_symbol = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.OtherClass",
            symbol_domain="other"
        )
        
        register.regist_symbol_path(detector_symbol)
        register.regist_symbol_path(other_symbol)
        
        # 搜索detector域的符号
        detector_results = register.search_symbol_data(domain="detector")
        assert len(detector_results) == 1
        assert detector_results[0] == detector_symbol
    
    def test_search_symbol_data_combined(self):
        """测试组合条件搜索符号"""
        register = DetectorPathRegister()
        
        # 清空现有符号并添加测试数据
        register._symbols = {}
        
        # 添加测试符号
        target_symbol = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.TargetClass",
            symbol_domain="detector"
        )
        other_symbol = SymbolModel(
            symbol_type=SymbolType.FUNCTION,
            symbol_path="ti.test.module.OtherFunction",
            symbol_domain="detector"
        )
        
        register.regist_symbol_path(target_symbol)
        register.regist_symbol_path(other_symbol)
        
        # 组合搜索：detector域中的类符号
        results = register.search_symbol_data(
            symbol_type=SymbolType.CLASS,
            domain="detector"
        )
        
        assert len(results) == 1
        assert results[0] == target_symbol
    
    def test_get_symbol_model(self):
        """测试获取所有符号模型"""
        register = DetectorPathRegister()
        
        # 清空现有符号并添加测试数据
        register._symbols = {}
        
        symbol1 = SymbolModel(
            symbol_type=SymbolType.CLASS,
            symbol_path="ti.test.module.Class1",
            symbol_domain="detector"
        )
        symbol2 = SymbolModel(
            symbol_type=SymbolType.FUNCTION,
            symbol_path="ti.test.module.function1",
            symbol_domain="detector"
        )
        
        register.regist_symbol_path(symbol1)
        register.regist_symbol_path(symbol2)
        
        all_symbols = register.get_symbol_model()
        
        assert len(all_symbols) == 2
        assert "class:ti.test.module.Class1" in all_symbols
        assert "function:ti.test.module.function1" in all_symbols
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.safe_load")
    def test_load_from_file_success(self, mock_yaml_load, mock_file_open):
        """测试成功从文件加载数据"""
        register = DetectorPathRegister()
        
        # 清空现有符号
        register._symbols = {}
        
        # 模拟YAML数据
        mock_data = {
            "classes": {
                "TestClass": {
                    "symbol_type": "class",
                    "symbol_path": "ti.test.module.TestClass",
                    "symbol_domain": "detector"
                }
            }
        }
        mock_yaml_load.return_value = mock_data
        
        # 调用内部加载方法
        register._load_from_file("test.yaml", "classes")
        
        # 验证符号被正确注册
        # 当symbol_name存在时，使用symbol_name作为key
        expected_id = "TestClass"
        assert expected_id in register._symbols
        
        symbol = register._symbols[expected_id]
        assert symbol.symbol_type == SymbolType.CLASS
        assert symbol.symbol_path == "ti.test.module.TestClass"
        assert symbol.symbol_domain == "detector"
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_from_file_not_found(self, mock_file_open):
        """测试文件不存在的情况"""
        register = DetectorPathRegister()
        
        # 清空现有符号
        register._symbols = {}
        
        # 应该不会抛出异常，只是打印警告
        register._load_from_file("nonexistent.yaml", "classes")
        
        # 验证符号字典仍然为空
        assert len(register._symbols) == 0
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.safe_load", side_effect=Exception("YAML parse error"))
    def test_load_from_file_parse_error(self, mock_yaml_load, mock_file_open):
        """测试YAML解析错误的情况"""
        register = DetectorPathRegister()
        
        # 清空现有符号
        register._symbols = {}
        
        # 应该不会抛出异常，只是打印错误信息
        register._load_from_file("corrupted.yaml", "classes")
        
        # 验证符号字典仍然为空
        assert len(register._symbols) == 0
    
    def test_load_data_integration(self, mocker):
        """测试完整的load_data集成"""
        register = DetectorPathRegister()
        
        # 清空现有符号
        register._symbols = {}
        
        # 模拟所有文件加载方法
        mock_load = mocker.patch.object(register, '_load_from_file')
        
        register.load_data()
        
        # 验证所有文件都被尝试加载
        assert mock_load.call_count == 4
        
        # 验证调用参数
        calls = mock_load.call_args_list
        expected_calls = [
            (("ti/features/detector/model/data/detector_class_methods.yaml", "class_methods"),),
            (("ti/features/detector/model/data/detector_functions.yaml", "functions"),),
            (("ti/features/detector/model/data/detector_classes.yaml", "classes"),),
            (("ti/features/detector/model/data/detector_enums.yaml", "enum_classes"),)
        ]
        
        for i, call in enumerate(calls):
            assert call[0] == expected_calls[i][0]