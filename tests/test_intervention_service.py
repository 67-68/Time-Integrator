import unittest
from unittest.mock import Mock, MagicMock

from ti.services.interventionService import InterventionService
from ti.services.realTimeMonitorService import RealTimeMonitor
from ti.features.intervention.presenter.interventionPresenter import InterventionPresenter

class TestInterventionService(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.mock_monitor = Mock(spec=RealTimeMonitor)
        self.service = InterventionService(monitor=self.mock_monitor)

    def test_initialization(self):
        """
        Test that the service initializes with an empty dictionary of interventions.
        """
        self.assertEqual(self.service.interventions, {})

    def test_create_intervention_creates_presenter_and_registers_with_monitor(self):
        """
        Test the core functionality: creating an InterventionPresenter and
        registering it with the RealTimeMonitor.
        """
        # GIVEN: An intervention initialization data packet
        mock_detector = Mock()
        mock_ui = Mock()
        intervention_init_pack = {
            "id": "intervention-123",
            "ui": mock_ui,
            "detector": mock_detector
        }

        # WHEN: create_intervention is called
        self.service.create_intervention(intervention_init_pack)

        # THEN:
        # 1. An InterventionPresenter should be created and stored.
        self.assertIn("intervention-123", self.service.interventions)
        presenter = self.service.interventions["intervention-123"]
        self.assertIsInstance(presenter, InterventionPresenter)
        self.assertEqual(presenter.ui, mock_ui)

        # 2. The monitor's add_monitor_project method should have been called once.
        self.mock_monitor.add_monitor_project.assert_called_once()

        # 3. The data passed to the monitor should be the correctly structured monitor_pack.
        expected_monitor_pack = {
            "id": "intervention-123",
            "ui": mock_ui,
            "detector": mock_detector
        }
        # We access the arguments passed to the mock method
        actual_call_args = self.mock_monitor.add_monitor_project.call_args[0][0]
        self.assertEqual(actual_call_args, expected_monitor_pack)

if __name__ == '__main__':
    unittest.main()
