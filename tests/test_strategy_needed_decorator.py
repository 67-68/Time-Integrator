import unittest
from typing import Protocol
from unittest.mock import Mock, patch

from ti.model.strategy.strategy_needed_decorator import strategy_needed
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


class TestStrategyNeededDecorator(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        # Clear the singleton instance to ensure clean state
        StrategyRepository._instance = None
        self.repo = StrategyRepository.get_instance()

    def tearDown(self):
        """Clean up after tests"""
        StrategyRepository._instance = None

    def test_decorator_injects_strategy(self):
        """Test that decorator injects the correct strategy"""
        # Register a strategy
        strategy_a = ConcreteStrategyA()
        contribution = StrategyContribution(
            strategy_id="test_strategy_a",
            strategy=strategy_a
        )
        self.repo.register_strategy(contribution)

        # Create decorated function
        @strategy_needed(TestStrategyProtocol)
        def test_function(data: str, strategy: TestStrategyProtocol) -> str:
            return strategy.execute(data)

        # Test the decorated function
        result = test_function("test_data")
        self.assertEqual(result, "StrategyA processed: test_data")

    def test_decorator_returns_none_when_no_strategy_found(self):
        """Test decorator behavior when no matching strategy is found"""
        # Repository is empty, no strategies registered

        @strategy_needed(TestStrategyProtocol)
        def test_function(data: str, strategy: TestStrategyProtocol) -> str:
            if strategy is None:
                return "No strategy found"
            return strategy.execute(data)

        # The decorator should pass None as strategy when no match is found
        result = test_function("test_data")
        self.assertEqual(result, "No strategy found")

    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves function name and docstring"""

        @strategy_needed(TestStrategyProtocol)
        def original_function(data: str, strategy: TestStrategyProtocol) -> str:
            """Original function docstring"""
            return "result"

        self.assertEqual(original_function.__name__, "original_function")
        self.assertEqual(original_function.__doc__, "Original function docstring")

    def test_multiple_strategies_first_match_returned(self):
        """Test that first matching strategy is returned when multiple exist"""
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

        @strategy_needed(TestStrategyProtocol)
        def test_function(data: str, strategy: TestStrategyProtocol) -> str:
            return strategy.execute(data)

        # Should return the first matching strategy (strategy_a)
        result = test_function("test_data")
        self.assertEqual(result, "StrategyA processed: test_data")

    def test_decorator_with_different_protocols(self):
        """Test decorator with different protocol types"""

        @runtime_checkable
        class AnotherProtocol(Protocol):
            def process(self, value: int) -> int:
                ...

        class AnotherStrategy:
            def process(self, value: int) -> int:
                return value * 2

        strategy = AnotherStrategy()
        contribution = StrategyContribution(
            strategy_id="another_strategy",
            strategy=strategy
        )
        self.repo.register_strategy(contribution)

        @strategy_needed(AnotherProtocol)
        def another_function(value: int, strategy: AnotherProtocol) -> int:
            return strategy.process(value)

        result = another_function(5)
        self.assertEqual(result, 10)

    def test_decorator_with_original_arguments(self):
        """Test that original function arguments are preserved"""
        strategy_a = ConcreteStrategyA()
        contribution = StrategyContribution(
            strategy_id="test_strategy",
            strategy=strategy_a
        )
        self.repo.register_strategy(contribution)

        @strategy_needed(TestStrategyProtocol)
        def complex_function(a: int, b: str, c: bool = True, strategy: TestStrategyProtocol = None) -> str:
            prefix = f"a={a}, b={b}, c={c}, "
            return prefix + strategy.execute("data")

        result = complex_function(1, "test", False)
        expected = "a=1, b=test, c=False, StrategyA processed: data"
        self.assertEqual(result, expected)

    @patch('ti.model.strategy.strategy_needed_decorator.StrategyRepository.get_instance')
    def test_decorator_uses_singleton_repository(self, mock_get_instance):
        """Test that decorator uses the singleton StrategyRepository"""
        mock_repo = Mock()
        mock_strategy = ConcreteStrategyA()
        mock_repo.get_strategy.return_value = mock_strategy
        mock_get_instance.return_value = mock_repo

        @strategy_needed(TestStrategyProtocol)
        def test_function(data: str, strategy: TestStrategyProtocol) -> str:
            return strategy.execute(data)

        test_function("test")

        # Verify that get_instance was called
        mock_get_instance.assert_called_once()
        # Verify that get_strategy was called with the correct protocol
        mock_repo.get_strategy.assert_called_once_with(TestStrategyProtocol)

    def test_decorator_with_none_protocol(self):
        """Test decorator behavior when protocol is None"""
        # This should print a warning but not crash
        with patch('builtins.print') as mock_print:
            @strategy_needed(None)
            def test_function(data: str, strategy) -> str:
                return "test"

            # The warning should be printed
            mock_print.assert_called_with("[WRAPPER]: must input a protocol")


if __name__ == '__main__':
    unittest.main()