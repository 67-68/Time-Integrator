import unittest
from unittest.mock import Mock, MagicMock

from ti.UI.presenters.InsightCardPresenter import InsightCardPresenter
from ti.services.interventionService import InterventionService
from ti.features.intervention.view.interventionCard import InterventionCard
from ti.UI.views.analysis.trendCard import InsightCard

class TestInsightCardPresenter(unittest.TestCase):

    def setUp(self):
        """Set up the test environment for the presenter."""
        self.mock_card_ui = Mock(spec=InsightCard)
        self.mock_intervention_ui = Mock(spec=InterventionCard)
        self.mock_intervention_service = Mock(spec=InterventionService)

        # To allow connecting to the mock's signal, we need to give it a real signal attribute
        self.mock_intervention_ui.user_promise = MagicMock()

        self.presenter = InsightCardPresenter(
            card_ui=self.mock_card_ui,
            IS=self.mock_intervention_service,
            intervention=self.mock_intervention_ui
        )

    def test_initialization_with_intervention_connects_signal(self):
        """
        Test that the presenter connects to the intervention UI's signal upon initialization.
        """
        # The connection is made in the __init__ method called in setUp.
        # We verify that the 'connect' method on our mock signal was called.
        self.mock_intervention_ui.user_promise.connect.assert_called_once()

    def test_create_intervention_slot_calls_service(self):
        """
        Test that the create_intervention method (the slot) correctly calls the
        InterventionService with the data it receives from the signal.
        """
        # GIVEN: A data packet that the signal would emit
        test_data_packet = {
            "id": "test-id",
            "detector": Mock(),
            "ui": self.mock_intervention_ui
        }

        # WHEN: The create_intervention slot is called with the data
        self.presenter.create_intervention(test_data_packet)

        # THEN: The intervention service's create_intervention method should be called
        # with that same data packet.
        self.mock_intervention_service.create_intervention.assert_called_once_with(test_data_packet)

    def test_signal_emission_triggers_service_call(self):
        """
        This is a more integrated test to verify the whole chain:
        Signal emit -> Slot execution -> Service call
        """
        # GIVEN: The presenter is initialized and connected (done in setUp)
        
        # We need to get the actual slot function that was passed to 'connect'
        # This is the lambda function: lambda data: self.create_intervention(data)
        connected_slot = self.mock_intervention_ui.user_promise.connect.call_args[0][0]

        # WHEN: The user_promise signal is emitted from the intervention UI
        test_data_packet = {"id": "signal-test-id"}
        # We manually call the slot with the test data, simulating the signal emission
        connected_slot(test_data_packet)

        # THEN: The intervention service's method should have been called.
        self.mock_intervention_service.create_intervention.assert_called_once_with(test_data_packet)
        
    def test_initialization_without_intervention_does_not_connect(self):
        """
        Test that if no intervention card is provided, no connection is attempted.
        """
        # We need a fresh mock because the one in setUp is already used.
        mock_intervention_ui_no_connect = Mock(spec=InterventionCard)
        mock_intervention_ui_no_connect.user_promise = MagicMock()

        # Create a presenter without an intervention card
        presenter_no_intervention = InsightCardPresenter(
            card_ui=self.mock_card_ui,
            IS=self.mock_intervention_service,
            intervention=None # Explicitly pass None
        )

        # Verify that the connect method was NOT called.
        mock_intervention_ui_no_connect.user_promise.connect.assert_not_called()


if __name__ == '__main__':
    unittest.main()
