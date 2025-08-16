import unittest
from unittest.mock import MagicMock
from ti.dataAccess.insightManager import InsightManager

class TestInsightManager(unittest.TestCase):
    def setUp(self):
        """Set up a mock InsightCacheService and an InsightManager instance."""
        self.mock_ics = MagicMock()
        self.manager = InsightManager(self.mock_ics)

    def test_duplicate_recipe_should_return_one_card(self):
        """
        Tests if the InsightManager correctly handles multiple insights from the same recipe (card_id),
        and only returns the one with the highest weight.
        """
        # Arrange: Define three cards from the same recipe with different weights.
        card_1_raw = {"card_id": "recipe_A", "data": "low"}
        card_1_pre = {"weight": 10, "content": "low"}

        card_2_raw = {"card_id": "recipe_A", "data": "high"}
        card_2_pre = {"weight": 100, "content": "high"}

        card_3_raw = {"card_id": "recipe_A", "data": "medium"}
        card_3_pre = {"weight": 50, "content": "medium"}
        
        # Another card from a different recipe to ensure it's not affected.
        card_B_raw = {"card_id": "recipe_B", "data": "other"}
        card_B_pre = {"weight": 99, "content": "other"}

        # Act: Add the cards to the manager.
        self.manager.add_card(card_1_raw, card_1_pre)
        self.manager.add_card(card_2_raw, card_2_pre)
        self.manager.add_card(card_3_raw, card_3_pre)
        self.manager.add_card(card_B_raw, card_B_pre)

        result_cards = self.manager.get_current_cards()

        # Assert: Check the results.
        # 1. There should be only two cards in the output.
        self.assertEqual(len(result_cards), 2, "Should return only two cards")

        # 2. The card for recipe_A should be the one with the highest weight (100).
        recipe_A_card = next((card for card in result_cards if card["content"] == "high"), None)
        self.assertIsNotNone(recipe_A_card, "The highest weight card for recipe_A should be present")
        self.assertEqual(recipe_A_card["weight"], 100)
        
        # 3. The card for recipe_B should be present.
        recipe_B_card = next((card for card in result_cards if card["content"] == "other"), None)
        self.assertIsNotNone(recipe_B_card, "The card for recipe_B should be present")

        # 4. Verify that all raw data was sent to the cache service.
        self.assertEqual(self.mock_ics.add_history_data.call_count, 4, "All raw cards should be archived")

if __name__ == '__main__':
    unittest.main()
