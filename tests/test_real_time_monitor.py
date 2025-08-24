import unittest
from unittest.mock import Mock, MagicMock

from PyQt6.QtCore import QObject, pyqtSignal

from ti.services.realTimeMonitorService import RealTimeMonitor
from ti.core.analysis.detectors.detector import BaseDetector

# Mock DataService for testing
class MockDataService(QObject):
    actionUnit_added = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

# Mock Detector for testing
class MockDetector(BaseDetector):
    pattern_detected = pyqtSignal(object)

    def __init__(self, config=None, services=None):
        # Provide a default config to satisfy the super().__init__
        if config is None:
            config = {"sequence": []}
        super().__init__(config, services)
        self.process_action_unit = Mock()

    def emit_pattern_detected(self, ui_obj):
        """Helper method to manually emit the signal for tests."""
        self.pattern_detected.emit(ui_obj)


class TestRealTimeMonitor(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.mock_ds = MockDataService()
        # We don't mock the connect method here to allow for more realistic testing
        self.monitor = RealTimeMonitor(DS=self.mock_ds)

    def test_initialization_connects_to_data_service(self):
        """
        Test if the monitor connects to the DataService's signal upon initialization.
        This is an indirect test. We'll verify by emitting the signal and checking the result.
        """
        # To test the connection, we'll add a project and then emit the signal.
        mock_detector = MockDetector()
        monitor_pack = {"detector": mock_detector, "ui": {}, "id": "test_id_1"}
        self.monitor.add_monitor_project(monitor_pack)

        test_action_unit = {"action": "test"}
        self.mock_ds.actionUnit_added.emit(test_action_unit)

        # If the connection was made in __init__, the detector's method should have been called.
        mock_detector.process_action_unit.assert_called_with(test_action_unit)


    def test_add_monitor_project_stores_project_and_connects_signal(self):
        """
        Test if a new monitor project is added correctly and its signal is connected.
        """
        mock_detector = MockDetector()
        # Spy on the connect method to verify the connection
        mock_detector.pattern_detected.connect = Mock()
        
        mock_ui = {"name": "Test UI"}
        monitor_pack = {
            "detector": mock_detector,
            "ui": mock_ui,
            "id": "test_id_1"
        }

        self.monitor.add_monitor_project(monitor_pack)

        # 1. Check if the project is stored
        self.assertIn("test_id_1", self.monitor.monitor_projects)
        self.assertEqual(self.monitor.monitor_projects["test_id_1"]["detector"], mock_detector)
        self.assertEqual(self.monitor.monitor_projects["test_id_1"]["ui"], mock_ui)

        # 2. Check if the detector's signal is connected
        mock_detector.pattern_detected.connect.assert_called_once()
        connected_slot = mock_detector.pattern_-detected.connect.call_args[0][0]
        self.assertEqual(connected_slot, self.monitor._on_pattern_detected)


    def test_monitor_triggers_all_detectors_on_action_recorded(self):
        """
        Test if the monitor calls all registered detectors' process methods.
        """
        # GIVEN: A monitor with multiple projects
        mock_detector1 = MockDetector()
        mock_detector2 = MockDetector()
        monitor_pack1 = {"detector": mock_detector1, "ui": {}, "id": "test_id_1"}
        monitor_pack2 = {"detector": mock_detector2, "ui": {}, "id": "test_id_2"}
        self.monitor.add_monitor_project(monitor_pack1)
        self.monitor.add_monitor_project(monitor_pack2)

        # WHEN: A new action unit is emitted from the data service
        test_action_unit = {"action": "multi-test"}
        self.mock_ds.actionUnit_added.emit(test_action_unit)

        # THEN: Both detectors should have been called
        mock_detector1.process_action_unit.assert_called_with(test_action_unit)
        mock_detector2.process_action_unit.assert_called_with(test_action_unit)


    def test_intervention_needed_signal_emitted_when_pattern_detected(self):
        """
        Test if the intervention_needed signal is emitted when a detector finds a pattern.
        """
        # GIVEN: A monitor with a project
        mock_detector = MockDetector()
        mock_ui = {"name": "Test UI Object"}
        monitor_pack = {"detector": mock_detector, "ui": mock_ui, "id": "test_id_1"}
        self.monitor.add_monitor_project(monitor_pack)

        # and a slot connected to the monitor's output signal
        mock_slot = Mock()
        self.monitor.intervention_needed.connect(mock_slot)

        # WHEN: The detector emits that it has found a pattern
        mock_detector.emit_pattern_detected(mock_ui)

        # THEN: The monitor's final signal should have been emitted with the correct UI object
        mock_slot.assert_called_once_with(mock_ui)


if __name__ == '__main__':
    unittest.main()
