import unittest
from typing import Protocol
from ti.services.serviceContainer import ServiceContainer
from ti.model.strategy.strategy_needed_decorator import strategy_needed
from ti.model.strategy.strategy_repository import StrategyRepository
from ti.model.strategy.strategy_contribution import StrategyContribution


from typing import runtime_checkable

@runtime_checkable
class TestIntegrationProtocol(Protocol):
    def process(self, data: str) -> str:
        ...


class IntegrationStrategy:
    def process(self, data: str) -> str:
        return f"Integration processed: {data}"


class TestStrategyRepositoryIntegration(unittest.TestCase):
    """集成测试：验证Service Container和装饰器使用同一个StrategyRepository实例"""

    def test_service_container_and_decorator_use_same_instance(self):
        """测试Service Container和装饰器使用同一个StrategyRepository实例"""

        # 创建Service Container（这会初始化StrategyRepository）
        service_container = ServiceContainer()

        # 从Service Container获取StrategyRepository实例
        strategy_repo_from_container = service_container.get_class_service(StrategyRepository)

        # 从装饰器使用的get_instance()获取实例
        strategy_repo_from_decorator = StrategyRepository.get_instance()

        # 验证它们是同一个实例
        self.assertIs(strategy_repo_from_container, strategy_repo_from_decorator,
                     "Service Container和装饰器应该使用同一个StrategyRepository实例")

    def test_strategy_registered_in_container_available_in_decorator(self):
        """测试在Service Container中注册的策略在装饰器中可用"""

        # 创建Service Container
        service_container = ServiceContainer()

        # 从Service Container获取StrategyRepository
        strategy_repo = service_container.get_class_service(StrategyRepository)

        # 注册一个策略
        strategy = IntegrationStrategy()
        contribution = StrategyContribution(
            strategy_id="integration_strategy",
            strategy=strategy
        )
        strategy_repo.register_strategy(contribution)

        # 使用装饰器，它应该能找到刚才注册的策略
        @strategy_needed(TestIntegrationProtocol)
        def test_function(data: str, strategy: TestIntegrationProtocol) -> str:
            return strategy.process(data)

        result = test_function("test_data")
        expected = "Integration processed: test_data"
        self.assertEqual(result, expected,
                        "装饰器应该能找到在Service Container中注册的策略")

    def test_singleton_pattern_works_correctly(self):
        """测试单例模式正常工作"""

        # 清除之前的实例
        StrategyRepository._instance = None

        # 多次调用get_instance应该返回同一个实例
        instance1 = StrategyRepository.get_instance()
        instance2 = StrategyRepository.get_instance()
        instance3 = StrategyRepository.get_instance()

        self.assertIs(instance1, instance2, "get_instance应该返回同一个实例")
        self.assertIs(instance2, instance3, "get_instance应该返回同一个实例")
        self.assertIs(instance1, instance3, "get_instance应该返回同一个实例")


if __name__ == '__main__':
    unittest.main()