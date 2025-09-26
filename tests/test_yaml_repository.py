import pytest
import tempfile
import os
import yaml
import json
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from ti.model.yaml_repository import YamlRepository


# 测试用的Pydantic模型
class TestContract(BaseModel):
    contract_id: UUID = Field(default_factory=uuid4)
    name: str
    status: str = "active"
    value: int = 0


class TestYamlRepository:
    
    def setup_method(self):
        # 创建临时文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # 创建repository实例
        self.repository = YamlRepository(self.db_path, TestContract)
    
    def teardown_method(self):
        # 清理临时文件
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
        # 清理可能的临时文件
        temp_json_path = self.db_path + '.temp.json'
        if os.path.exists(temp_json_path):
            os.unlink(temp_json_path)
    
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
        assert isinstance(result, TestContract)
        assert result.name == "test_contract"
        assert result.value == 100
        assert result.contract_id == contract.contract_id
    
    def test_get_by_id_not_found(self):
        """测试获取不存在的ID"""
        result = self.repository.get_by_id(uuid4())
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
        assert result.value == 100
        assert result.name == "initial"
    
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
        assert all(isinstance(item, TestContract) for item in all_data)
        names = [item.name for item in all_data]
        assert "contract1" in names
        assert "contract2" in names
    
    def test_load(self):
        """测试load方法"""
        contract = TestContract(name="test_load")
        self.repository.save(contract)
        
        data = self.repository.load()
        assert len(data) == 1
        assert isinstance(data[0], TestContract)
        assert data[0].name == "test_load"
    
    def test_delete(self):
        """测试删除记录"""
        contract = TestContract(name="to_delete")
        self.repository.save(contract)
        
        # 验证记录存在
        assert self.repository.exists(str(contract.contract_id))
        
        # 删除记录
        self.repository.delete(str(contract.contract_id))
        
        # 验证记录已删除
        assert not self.repository.exists(str(contract.contract_id))
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
        assert isinstance(active_contracts[0], TestContract)
        assert active_contracts[0].name == "active_contract"
        
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
        self.repository.update_field(str(contract.contract_id), "value", 100)
        
        result = self.repository.get_by_id(contract.contract_id)
        assert result.value == 100
        assert result.name == "original"  # 其他字段保持不变
    
    def test_exists(self):
        """测试存在性检查"""
        contract = TestContract(name="test_exists")
        
        # 检查不存在的记录
        assert not self.repository.exists(str(contract.contract_id))
        
        # 保存后检查
        self.repository.save(contract)
        assert self.repository.exists(str(contract.contract_id))


class TestYamlRepositoryWithYamlFile:
    
    def setup_method(self):
        # 创建临时YAML文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.yaml', delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # 创建初始YAML数据
        initial_data = [
            {
                "contract_id": "12345678-1234-1234-1234-123456789abc",
                "name": "existing_contract",
                "status": "active",
                "value": 50
            }
        ]
        
        with open(self.db_path, 'w', encoding='utf-8') as f:
            yaml.dump(initial_data, f, allow_unicode=True, default_flow_style=False, indent=2)
        
        # 创建repository实例
        self.repository = YamlRepository(self.db_path, TestContract)
    
    def teardown_method(self):
        # 清理临时文件
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
        # 清理可能的临时文件
        temp_json_path = self.db_path + '.temp.json'
        if os.path.exists(temp_json_path):
            os.unlink(temp_json_path)
    
    def test_yaml_file_detection(self):
        """测试YAML文件检测"""
        # 应该检测到这是YAML文件
        assert self.repository.is_yaml_file is True
    
    def test_load_from_yaml(self):
        """测试从YAML文件加载数据"""
        data = self.repository.get_all()
        assert len(data) == 1
        assert isinstance(data[0], TestContract)
        assert data[0].name == "existing_contract"
        assert data[0].value == 50
    
    def test_save_to_yaml(self):
        """测试保存数据到YAML文件"""
        # 添加新数据
        new_contract = TestContract(name="new_contract", value=100)
        self.repository.save(new_contract)
        
        # 验证数据已保存
        data = self.repository.get_all()
        assert len(data) == 2
        
        # 验证YAML文件内容
        with open(self.db_path, 'r', encoding='utf-8') as f:
            yaml_content = yaml.safe_load(f)
        
        assert len(yaml_content) == 2
        assert yaml_content[1]["name"] == "new_contract"
    
    def test_yaml_file_preserved(self):
        """测试YAML文件格式被保留"""
        # 验证原文件仍然是YAML格式
        with open(self.db_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含YAML特征（如缩进、冒号等）
        assert ':' in content
        assert content.strip().startswith('-')  # YAML列表格式


class TestYamlRepositoryWithJsonFile:
    
    def setup_method(self):
        # 创建临时JSON文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        
        # 创建初始JSON数据
        initial_data = [
            {
                "contract_id": "12345678-1234-1234-1234-123456789abc",
                "name": "existing_contract",
                "status": "active",
                "value": 50
            }
        ]
        
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        
        # 创建repository实例
        self.repository = YamlRepository(self.db_path, TestContract)
    
    def teardown_method(self):
        # 清理临时文件
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_json_file_detection(self):
        """测试JSON文件检测"""
        # 应该检测到这是JSON文件
        assert self.repository.is_yaml_file is False
    
    def test_load_from_json(self):
        """测试从JSON文件加载数据"""
        data = self.repository.get_all()
        assert len(data) == 1
        assert isinstance(data[0], TestContract)
        assert data[0].name == "existing_contract"
        assert data[0].value == 50