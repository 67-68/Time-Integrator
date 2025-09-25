import pytest
import tempfile
import os
from uuid import uuid4
from unittest.mock import Mock
from pydantic import BaseModel, Field

from ti.model.yaml_repository import YamlRepository


# 测试用的Pydantic模型
class TestContract(BaseModel):
    contract_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    status: str = "active"
    value: int = 0


class TestTinyDbContractRepository:
    
    def setup_method(self):
        # 创建临时文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # 创建repository实例
        self.repository = YamlRepository(self.db_path)
    
    def teardown_method(self):
        # 清理临时文件
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_save_and_get_by_id(self):
        """测试保存和根据ID获取"""
        # 创建测试数据
        contract = TestContract(name="test_contract", value=100)
        
        # 保存数据
        self.repository.save(contract)
        
        # 根据ID获取数据
        result = self.repository.get_by_id(contract.contract_id)
        
        # 验证结果
        assert result is not None
        assert result['name'] == "test_contract"
        assert result['value'] == 100
        assert result['contract_id'] == contract.contract_id
    
    def test_get_by_id_not_found(self):
        """测试获取不存在的ID"""
        result = self.repository.get_by_id("non_existent_id")
        assert result is None
    
    def test_save_update_existing(self):
        """测试更新现有记录"""
        # 创建并保存初始数据
        contract = TestContract(name="initial", value=50)
        self.repository.save(contract)
        
        # 更新数据
        contract.value = 100
        self.repository.save(contract)
        
        # 验证更新
        result = self.repository.get_by_id(contract.contract_id)
        assert result['value'] == 100
        assert result['name'] == "initial"
    
    def test_get_all(self):
        """测试获取所有数据"""
        # 创建多个测试数据
        contract1 = TestContract(name="contract1")
        contract2 = TestContract(name="contract2")
        
        self.repository.save(contract1)
        self.repository.save(contract2)
        
        # 获取所有数据
        all_data = self.repository.get_all()
        
        # 验证结果
        assert len(all_data) == 2
        names = [item['name'] for item in all_data]
        assert "contract1" in names
        assert "contract2" in names
    
    def test_load(self):
        """测试load方法"""
        contract = TestContract(name="test_load")
        self.repository.save(contract)
        
        data = self.repository.load()
        assert len(data) == 1
        assert data[0]['name'] == "test_load"
    
    def test_delete(self):
        """测试删除记录"""
        contract = TestContract(name="to_delete")
        self.repository.save(contract)
        
        # 验证记录存在
        assert self.repository.exists(contract.contract_id)
        
        # 删除记录
        self.repository.delete(contract.contract_id)
        
        # 验证记录已删除
        assert not self.repository.exists(contract.contract_id)
        assert self.repository.get_by_id(contract.contract_id) is None
    
    def test_query(self):
        """测试条件查询"""
        # 创建不同状态的数据
        contract1 = TestContract(name="active_contract", status="active")
        contract2 = TestContract(name="inactive_contract", status="inactive")
        
        self.repository.save(contract1)
        self.repository.save(contract2)
        
        # 查询活跃状态的合同
        active_contracts = self.repository.query(status="active")
        assert len(active_contracts) == 1
        assert active_contracts[0]['name'] == "active_contract"
        
        # 查询不存在的状态
        empty_result = self.repository.query(status="pending")
        assert len(empty_result) == 0
    
    def test_count(self):
        """测试计数功能"""
        assert self.repository.count() == 0
        
        contract = TestContract(name="test_count")
        self.repository.save(contract)
        
        assert self.repository.count() == 1
    
    def test_clear(self):
        """测试清空数据"""
        contract = TestContract(name="test_clear")
        self.repository.save(contract)
        
        assert self.repository.count() == 1
        
        self.repository.clear()
        
        assert self.repository.count() == 0
    
    def test_update_field(self):
        """测试更新特定字段"""
        contract = TestContract(name="original", value=50)
        self.repository.save(contract)
        
        # 更新value字段
        self.repository.update_field(contract.contract_id, "value", 100)
        
        result = self.repository.get_by_id(contract.contract_id)
        assert result['value'] == 100
        assert result['name'] == "original"  # 其他字段保持不变
    
    def test_exists(self):
        """测试存在性检查"""
        contract = TestContract(name="test_exists")
        
        # 检查不存在的记录
        assert not self.repository.exists(contract.contract_id)
        
        # 保存后检查
        self.repository.save(contract)
        assert self.repository.exists(contract.contract_id)
    
    def test_rule_file_path_property(self):
        """测试规则文件路径属性"""
        expected_path = self.db_path.replace('.json', '_rules.yaml')
        assert self.repository.rule_file_path == expected_path
    
    def test_yaml_parser_property(self):
        """测试yaml parser属性"""
        # 默认情况下应该为None
        assert self.repository.yaml is None
        
        # 测试传入yaml parser的情况
        mock_parser = Mock()
        repo_with_parser = YamlRepository(self.db_path, mock_parser)
        assert repo_with_parser.yaml == mock_parser