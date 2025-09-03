import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from ti.features.intervention.model.model import INV_Contract, INV_Contract_Duration, INV_Contract_State, INV_ContractLog
from ti.features.intervention.service.contractService import INV_ContractService
from ti.features.intervention.service.logger import InterventionLogger


class TestContractDurationCheck:
    """测试 Contract 过期检查功能"""
    
    def test_today_contract_not_expired(self, contract_service, sample_contract):
        """测试: TODAY类型的contract在当天内不应该过期"""
        # Given: 一个今天创建的contract
        
        # When: 检查是否过期
        is_expired = contract_service.contract_duration_check(sample_contract)
        
        # Then: 应该没有过期
        assert not is_expired
    
    def test_today_contract_expired_after_midnight(self, contract_service):
        """测试: TODAY类型的contract在过了午夜后应该过期"""
        # Given: 一个昨天创建的TODAY类型contract
        yesterday = datetime.now() - timedelta(days=1, hours=2)
        contract = INV_Contract(
            contract_category_id="test",
            duration=INV_Contract_Duration.TODAY.value,
            current_state=INV_Contract_State.AGREED.value,
            create_time=yesterday
        )
        
        # When: 检查是否过期
        is_expired = contract_service.contract_duration_check(contract)
        
        # Then: 应该已过期
        assert is_expired
    
    def test_to_tomorrow_contract_expired_after_24h(self, contract_service):
        """测试: TO_TOMORROW类型的contract在24小时后过期"""
        # Given: 一个超过24小时前创建的contract
        over_24h_ago = datetime.now() - timedelta(hours=25)
        contract = INV_Contract(
            contract_category_id="test",
            duration=INV_Contract_Duration.TO_TOMORROW.value,
            current_state=INV_Contract_State.AGREED.value,
            create_time=over_24h_ago
        )
        
        # When: 检查是否过期
        is_expired = contract_service.contract_duration_check(contract)
        
        # Then: 应该已过期
        assert is_expired
    
    def test_this_week_contract_not_expired(self, contract_service):
        """测试: THIS_WEEK类型的contract在本周内不应该过期"""
        # Given: 一个本周创建的contract
        contract = INV_Contract(
            contract_category_id="test",
            duration=INV_Contract_Duration.THIS_WEEK.value,
            current_state=INV_Contract_State.AGREED.value,
            create_time=datetime.now() - timedelta(days=2)  # 2天前创建
        )
        
        # When: 检查是否过期
        is_expired = contract_service.contract_duration_check(contract)
        
        # Then: 应该没有过期（假设还在本周内）
        assert not is_expired


class TestInterventionLogger:
    """测试干涉日志记录功能"""
    
    def test_log_contract_creates_log_entry(self):
        """测试: log_contract 能正确创建日志条目"""
        # Given: 一个contract和mock repository
        contract = INV_Contract(
            contract_category_id="post_eat_waste",
            duration=INV_Contract_Duration.TODAY.value,
            current_state=INV_Contract_State.AGREED.value
        )
        mock_repository = MagicMock()
        logger = InterventionLogger(mock_repository)
        
        # When: 归档contract
        log_id = logger.log_contract(contract, "completed")
        
        # Then: 应该调用repository保存日志
        mock_repository.add_log.assert_called_once()
        assert log_id is not None
    
    def test_convert_contract_to_log_preserves_key_data(self):
        """测试: contract转log时保留关键数据"""
        # Given: 一个contract
        contract = INV_Contract(
            contract_category_id="post_eat_waste",
            duration=INV_Contract_Duration.TODAY.value,
            current_state=INV_Contract_State.AGREED.value
        )
        logger = InterventionLogger()
        
        # When: 转换为log
        log = logger._convert_contract_to_log(contract, "completed")
        
        # Then: 关键信息应该被保留
        assert log.original_contract_id == contract.contract_uuid
        assert log.original_contract_category_id == contract.contract_category_id
        assert log.final_willingness_status == "accepted"
        assert log.final_execution_status == "completed"
        assert log.created_at == contract.create_time
    
    def test_get_willingness_status_mapping(self):
        """测试: 意愿状态映射是否正确"""
        logger = InterventionLogger()
        
        # Test accepted cases
        agreed_contract = INV_Contract(current_state=INV_Contract_State.AGREED.value)
        assert logger._get_willingness_status(agreed_contract) == "accepted"
        
        # Test declined case  
        declined_contract = INV_Contract(current_state="declined")
        assert logger._get_willingness_status(declined_contract) == "declined"
        
        # Test unknown case
        unknown_contract = INV_Contract(current_state="unknown_state")
        assert logger._get_willingness_status(unknown_contract) == "unknown"


class TestContractLifeCycle:
    """测试 Contract 生命周期管理"""
    
    def test_expired_contract_gets_logged_and_deleted(self, contract_service, expired_contract):
        """测试: 过期的contract会被归档并删除"""
        # Given: 一个过期的contract
        
        # When: 运行生命周期检查
        result = contract_service.runLifeCycle(expired_contract)
        
        # Then: contract应该被归档和删除
        contract_service.logger.log_contract.assert_called_once_with(expired_contract)
        contract_service.contract_rep.delete.assert_called_once()
        assert result is None  # 被删除的contract不返回
    
    def test_active_contract_gets_monitored(self, contract_service, sample_contract):
        """测试: 活跃的contract会被添加到监控"""
        # Given: 一个agreed状态的contract
        
        # When: 运行生命周期检查
        result = contract_service.runLifeCycle(sample_contract)
        
        # Then: contract应该被添加到监控
        contract_service.register.add_monitor_project.assert_called_once()
        contract_service.contract_rep.add_contract.assert_called_once()