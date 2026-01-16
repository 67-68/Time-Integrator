import unittest
from typing import Protocol
from unittest.mock import Mock, patch

from ti.services.strategy_service import StrategyService
from ti.model.strategy.strategy_repository import StrategyRepository
from ti.model.strategy.strategy_contribution import StrategyContribution


from typing import runtime_checkable


@runtime_checkable
class TestStrategyProtocol(Protocol):
    """Test protocol for strategy pattern"""
    def execute(self, data: str) -> str:
        ...


class ConcreteStrategyA:
    """Concrete implementation of TestStrategyProtocol"""
    def execute(self, data: str) -> str:
        return f"StrategyA processed: {data}"


class ConcreteStrategyB:
    """Another concrete implementation"""
    def execute(self, data: str) -> str:
        return f"StrategyB processed: {data}"


class InvalidStrategy:
    """Strategy that doesn't implement the protocol method"""
    def wrong_method(self, data: str) -> str:
        return f"Wrong method: {data}"


class TestStrategyService(unittest.TestCase):
    """Test cases for StrategyService"""

    def setUp(self):
        """Set up test environment"""
        # Clear the singleton instance to ensure clean state
        StrategyRepository._instance = None
        self.repo = StrategyRepository.get_instance()

    def tearDown(self):
        """Clean up after tests"""
        StrategyRepository._instance = None

    def test_execute_with_strategy_when_strategy_available(self):
        """Test execute_with_strategy when a strategy is available"""
        # Register a strategy
        strategy_a = ConcreteStrategyA()
        contribution = StrategyContribution(
            strategy_id="test_strategy_a",
            strategy=strategy_a
        )
        self.repo.register_strategy(contribution)

        # Define a default function
        def default_function(data: str) -> str:
            return f"Default processed: {data}"

        # Test with strategy available
        result = StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        self.assertEqual(result, "StrategyA processed: test_data")

    def test_execute_with_strategy_when_no_strategy_available(self):
        """Test execute_with_strategy when no strategy is available"""
        # Repository is empty, no strategies registered

        # Define a default function
        def default_function(data: str) -> str:
            return f"Default processed: {data}"

        # Test with no strategy available
        result = StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        self.assertEqual(result, "Default processed: test_data")

    def test_execute_with_strategy_with_multiple_arguments(self):
        """Test execute_with_strategy with multiple arguments - demonstrates current behavior where all args are passed to strategy"""
        # Create a strategy that can handle multiple arguments
        @runtime_checkable
        class MultiArgProtocol(Protocol):
            def execute(self, data: str, count: int, flag: bool) -> str:
                ...

        class MultiArgStrategy:
            def execute(self, data: str, count: int, flag: bool) -> str:
                status = "enabled" if flag else "disabled"
                return f"Strategy: {data} x{count} ({status})"

        # Register the multi-argument strategy
        strategy = MultiArgStrategy()
        contribution = StrategyContribution(
            strategy_id="multi_arg_strategy",
            strategy=strategy
        )
        self.repo.register_strategy(contribution)

        # Define a default function with multiple arguments
        def default_function(data: str, count: int, flag: bool) -> str:
            status = "enabled" if flag else "disabled"
            return f"Default: {data} x{count} ({status})"

        # Test with multiple arguments - all arguments are passed to strategy
        result = StrategyService.execute_with_strategy(
            MultiArgProtocol,
            default_function,
            "test_data",
            3,
            True
        )

        # Strategy receives all arguments
        self.assertEqual(result, "Strategy: test_data x3 (enabled)")

    def test_execute_with_strategy_with_keyword_arguments(self):
        """Test execute_with_strategy with keyword arguments - strategy should only receive positional arguments"""
        # Register a strategy
        strategy_a = ConcreteStrategyA()
        contribution = StrategyContribution(
            strategy_id="test_strategy_a",
            strategy=strategy_a
        )
        self.repo.register_strategy(contribution)

        # Define a default function with keyword arguments
        def default_function(data: str, multiplier: int = 1) -> str:
            return f"Default: {data} x{multiplier}"

        # Test with keyword arguments - strategy should only receive positional arguments
        result = StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        self.assertEqual(result, "StrategyA processed: test_data")

    def test_invoke_method_from_protocol_success(self):
        """Test _invoke_method_from_protocol with valid strategy"""
        strategy = ConcreteStrategyA()

        method = StrategyService._invoke_method_from_protocol(strategy, TestStrategyProtocol)

        # Verify the method is callable and works correctly
        self.assertTrue(callable(method))
        result = method("test_data")
        self.assertEqual(result, "StrategyA processed: test_data")

    def test_invoke_method_from_protocol_no_public_methods(self):
        """Test _invoke_method_from_protocol with protocol that has no public methods"""

        @runtime_checkable
        class EmptyProtocol(Protocol):
            """Protocol with no public methods"""
            def _private_method(self):
                ...

        strategy = ConcreteStrategyA()

        with self.assertRaises(AttributeError) as context:
            StrategyService._invoke_method_from_protocol(strategy, EmptyProtocol)

        self.assertIn("没有找到任何公开方法", str(context.exception))

    def test_invoke_method_from_protocol_method_not_implemented(self):
        """Test _invoke_method_from_protocol when strategy doesn't implement the method"""
        # Use the class instead of instance since the service expects __name__ attribute
        strategy = InvalidStrategy

        with self.assertRaises(NotImplementedError) as context:
            StrategyService._invoke_method_from_protocol(strategy, TestStrategyProtocol)

        self.assertIn("中没有实现 protocol", str(context.exception))
        self.assertIn("execute 方法", str(context.exception))

    def test_invoke_method_from_protocol_with_different_protocol(self):
        """Test _invoke_method_from_protocol with a different protocol"""

        @runtime_checkable
        class DifferentProtocol(Protocol):
            def transform(self, value: int) -> int:
                ...

        class DifferentStrategy:
            def transform(self, value: int) -> int:
                return value * 2

        strategy = DifferentStrategy()

        method = StrategyService._invoke_method_from_protocol(strategy, DifferentProtocol)
        result = method(5)

        self.assertEqual(result, 10)

    @patch('ti.services.strategy_service.StrategyRepository.get_instance')
    def test_execute_with_strategy_uses_repository(self, mock_get_instance):
        """Test that execute_with_strategy uses StrategyRepository correctly"""
        mock_repo = Mock()
        mock_strategy = ConcreteStrategyA()
        mock_repo.get_strategy.return_value = mock_strategy
        mock_get_instance.return_value = mock_repo

        def default_function(data: str) -> str:
            return f"Default: {data}"

        StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        # Verify that get_instance was called
        mock_get_instance.assert_called_once()
        # Verify that get_strategy was called with the correct protocol
        mock_repo.get_strategy.assert_called_once_with(TestStrategyProtocol)

    def test_execute_with_strategy_multiple_strategies_first_match(self):
        """Test execute_with_strategy returns first matching strategy when multiple exist"""
        # Register multiple strategies
        strategy_a = ConcreteStrategyA()
        strategy_b = ConcreteStrategyB()

        contribution_a = StrategyContribution(
            strategy_id="strategy_a",
            strategy=strategy_a
        )
        contribution_b = StrategyContribution(
            strategy_id="strategy_b",
            strategy=strategy_b
        )

        self.repo.register_strategy(contribution_a)
        self.repo.register_strategy(contribution_b)

        def default_function(data: str) -> str:
            return f"Default: {data}"

        # Should return the first matching strategy (strategy_a)
        result = StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        self.assertEqual(result, "StrategyA processed: test_data")

    def test_execute_with_strategy_return_value_preserved(self):
        """Test that execute_with_strategy preserves return values correctly"""
        # Register a strategy
        strategy_a = ConcreteStrategyA()
        contribution = StrategyContribution(
            strategy_id="test_strategy_a",
            strategy=strategy_a
        )
        self.repo.register_strategy(contribution)

        # Define a default function that returns a complex object
        def default_function(data: str) -> dict:
            return {"status": "default", "data": data}

        # Test with strategy available
        result = StrategyService.execute_with_strategy(
            TestStrategyProtocol,
            default_function,
            "test_data"
        )

        # Should return the strategy result, not the default function result
        self.assertEqual(result, "StrategyA processed: test_data")


if __name__ == '__main__':
    unittest.main()