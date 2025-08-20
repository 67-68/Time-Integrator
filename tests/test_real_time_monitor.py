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
    # Re-implement pattern_detected as a class attribute for mocking
    pattern_detected = pyqtSignal(object)

    def __init__(self, config=None, services=None):
        super().__init__(config, services)
        # Mock the process_action_unit method
        self.process_action_unit = Mock()

    def emit_pattern_detected(self, ui_obj):
        """Helper method to manually emit the signal for tests."""
        self.pattern_detected.emit(ui_obj)


class TestRealTimeMonitor(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.mock_ds = MockDataService()
        # It's better to pass the real object to connect, 
        # but mock its methods if needed.
        # Here we spy on the connect method.
        self.mock_ds.actionUnit_added.connect = Mock()
        
        self.monitor = RealTimeMonitor(DS=self.mock_ds)
        
        # Restore the original connect method after __init__
        # This is a bit of a workaround to verify the connection call.
        # A better approach might be dependency injection for the signal itself.
        self.mock_ds.actionUnit_added.connect = self.mock_ds.actionUnit_added.connect

    def test_initialization_connects_to_data_service(self):
        """
        Test if the monitor connects to the DataService's signal upon initialization.
        """
        # We mocked 'connect' in setUp to check if it was called.
        # Let's re-check the mock object that was used during init.
        mock_connect = self.monitor.DS.actionUnit_added.connect
        mock_connect.assert_called_once()
        # Check that it's connected to the right slot
        connected_slot = mock_connect.call_args[0][0]
        self.assertTrue(callable(connected_slot))


    def test_add_monitor_project_stores_project_and_connects_signal(self):
        """
        Test if a new monitor project is added correctly and its signal is connected.
        """
        mock_detector = MockDetector()
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
        connected_slot = mock_detector.pattern_detected.connect.call_args[0][0]
        self.assertTrue(callable(connected_slot))


    def test_monitor_triggers_detector_on_action_recorded(self):
        """
        Test if the monitor calls the detector's process method when an action is recorded.
        """
        mock_detector = MockDetector()
        monitor_pack = {"detector": mock_detector, "ui": {}, "id": "test_id_1"}
        self.monitor.add_monitor_project(monitor_pack)

        test_action_unit = {"action": "test"}
        
        # Manually connect the signal for the test since we mocked it in setUp
        self.monitor.DS.actionUnit_added.connect(self.monitor._on_action_recorded)
        self.monitor.DS.actionUnit_added.emit(test_action_unit)

        # Verify that the detector's process method was called with the action unit
        mock_detector.process_action_unit.assert_called_with(test_action_unit)


    def test_intervention_needed_signal_emitted_when_pattern_detected(self):
        """
        Test if the intervention_needed signal is emitted when a detector finds a pattern.
        """
        mock_detector = MockDetector()
        mock_ui = {"name": "Test UI Object"}
        monitor_pack = {"detector": mock_detector, "ui": mock_ui, "id": "test_id_1"}
        
        self.monitor.add_monitor_project(monitor_pack)

        # Mock the slot that will receive the final signal
        mock_slot = Mock()
        self.monitor.intervention_needed.connect(mock_slot)

        # Manually trigger the detector's signal, simulating a pattern match
        mock_detector.emit_pattern_detected(mock_ui)

        # Verify that the final signal was emitted with the correct UI object
        mock_slot.assert_called_once_with(mock_ui)


if __name__ == '__main__':
    unittest.main()
