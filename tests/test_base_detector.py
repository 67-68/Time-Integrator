import pytest
from unittest.mock import Mock, MagicMock
from ti.features.detector.baseDetector import BaseDetector
from ti.features.detector.model import Detector_Config, Detector_Sequence, Detector_State, BaseDetectorState
from ti.features.detector.matchers import Matcher
from ti.services.dataAccess.insightCacheService import InsightCacheService


def create_test_detector_config():
    """Create a test detector configuration with simple matchers"""
    matcher = Matcher()
    
    # Hook states - match action "start_work"
    hook_state_1 = Detector_State(
        state_name="hook_start",
        matcher=matcher.action_is("start_work")
    )
    
    # Result states - match action_type "work"
    result_state_1 = Detector_State(
        state_name="result_work",
        matcher=matcher.action_type_is("work")
    )
    result_state_2 = Detector_State(
        state_name="result_work_2", 
        matcher=matcher.action_type_is("work")
    )
    
    sequence = Detector_Sequence(
        hook=[hook_state_1],
        result=[result_state_1, result_state_2]
    )
    
    config = Detector_Config(sequence=sequence)
    config.card_type_id = "test_detector"
    
    return config


class TestBaseDetector:
    
    @staticmethod
    def create_mock_action_unit(action="test_action", action_type="work", start="10:00", end="10:30", timeSpan=30):
        """Create a mock action unit for testing"""
        return {
            "action": action,
            "action_type": action_type,
            "start": start,
            "end": end,
            "timeSpan": timeSpan,
            "uid": "test_uid_123"
        }
    
    def setup_method(self):
        """Setup before each test"""
        self.mock_insight_cache = Mock(spec=InsightCacheService)
        self.mock_insight_cache.create_new_data.return_value = {
            "weight": 0,
            "history": {},
            "id": "",
            "data": [],
            "card_id": "test_card_id"
        }
        self.mock_insight_cache.get_history_data.return_value = {}
        
        self.config = create_test_detector_config()
        self.detector = BaseDetector(self.config, self.mock_insight_cache)
        
        # Mock signals to track emissions
        self.hook_signal_calls = []
        self.pattern_signal_calls = []
        
        self.detector.hook_pattern_detected.connect(
            lambda data: self.hook_signal_calls.append(data)
        )
        self.detector.pattern_detected.connect(
            lambda data: self.pattern_signal_calls.append(data)
        )
    
    def test_initial_state(self):
        """Test that detector starts in HOOK state with index 0"""
        assert self.detector.currentState == BaseDetectorState.HOOK.value
        assert self.detector.currentIndex == 0
        assert self.detector.passed_au == {}
    
    def test_hook_state_transition(self):
        """Test successful transition from HOOK to RESULT state"""
        # Create action unit that matches hook condition
        hook_au = self.create_mock_action_unit(action="start_work")
        
        # Process hook action unit
        self.detector.process_action_unit(hook_au)
        
        # Should transition to RESULT state
        assert self.detector.currentState == BaseDetectorState.RESULT.value
        assert self.detector.currentIndex == 0
        assert len(self.hook_signal_calls) == 1
        assert "hook_start" in self.detector.passed_au
    
    def test_complete_pattern_detection(self):
        """Test complete pattern detection from HOOK to final RESULT"""
        # Hook phase
        hook_au = self.create_mock_action_unit(action="start_work")
        self.detector.process_action_unit(hook_au)
        
        # Result phase - first result
        result_au_1 = self.create_mock_action_unit(action_type="work")
        self.detector.process_action_unit(result_au_1)
        
        # Should still be in RESULT state with index 1
        assert self.detector.currentState == BaseDetectorState.RESULT.value
        assert self.detector.currentIndex == 1
        assert len(self.pattern_signal_calls) == 0  # Not complete yet
        
        # Result phase - second result (completes the pattern)
        result_au_2 = self.create_mock_action_unit(action_type="work")
        self.detector.process_action_unit(result_au_2)
        
        # Should reset and emit pattern detected signal
        assert self.detector.currentState == BaseDetectorState.HOOK.value
        assert self.detector.currentIndex == 0
        assert len(self.pattern_signal_calls) == 1
        assert len(self.detector.passed_au) == 3  # hook + 2 results
    
    def test_failed_hook_resets(self):
        """Test that failed hook match resets the detector"""
        # Process action unit that doesn't match hook
        non_matching_au = self.create_mock_action_unit(action="wrong_action")
        self.detector.process_action_unit(non_matching_au)
        
        # Should remain in initial state
        assert self.detector.currentState == BaseDetectorState.HOOK.value
        assert self.detector.currentIndex == 0
        assert self.detector.passed_au == {}
    
    def test_failed_result_resets(self):
        """Test that failed result match at index 0 doesn't reset (current implementation)"""
        # Successful hook
        hook_au = self.create_mock_action_unit(action="start_work")
        self.detector.process_action_unit(hook_au)
        
        # Failed result (wrong action type) at index 0 - should NOT reset
        failed_result_au = self.create_mock_action_unit(action_type="rest")
        self.detector.process_action_unit(failed_result_au)
        
        # Should remain in RESULT state at index 0 (current implementation behavior)
        # Reset only happens when currentIndex > 0
        assert self.detector.currentState == BaseDetectorState.RESULT.value
        assert self.detector.currentIndex == 0
        # passed_au should still contain the hook
        assert "hook_start" in self.detector.passed_au
    
    def test_multiple_successful_detections(self):
        """Test that detector can detect multiple patterns sequentially"""
        # First complete pattern
        hook_au_1 = self.create_mock_action_unit(action="start_work")
        result_au_1 = self.create_mock_action_unit(action_type="work")
        result_au_2 = self.create_mock_action_unit(action_type="work")
        
        self.detector.process_action_unit(hook_au_1)
        self.detector.process_action_unit(result_au_1)
        self.detector.process_action_unit(result_au_2)
        
        assert len(self.pattern_signal_calls) == 1
        
        # Second complete pattern
        hook_au_2 = self.create_mock_action_unit(action="start_work")
        result_au_3 = self.create_mock_action_unit(action_type="work")
        result_au_4 = self.create_mock_action_unit(action_type="work")
        
        self.detector.process_action_unit(hook_au_2)
        self.detector.process_action_unit(result_au_3)
        self.detector.process_action_unit(result_au_4)
        
        assert len(self.pattern_signal_calls) == 2
        assert self.detector.currentState == BaseDetectorState.HOOK.value
        assert self.detector.currentIndex == 0
    
    def test_packer_function(self):
        """Test that packer correctly packages data with weight calculation"""
        # Complete a pattern to populate passed_au
        hook_au = self.create_mock_action_unit(action="start_work", timeSpan=10)
        result_au_1 = self.create_mock_action_unit(action_type="work", timeSpan=20)
        result_au_2 = self.create_mock_action_unit(action_type="work", timeSpan=30)
        
        self.detector.process_action_unit(hook_au)
        self.detector.process_action_unit(result_au_1)
        self.detector.process_action_unit(result_au_2)
        
        # Get packed data from the signal call
        packed_data = self.pattern_signal_calls[0]
        
        # Verify packed data structure
        assert packed_data["weight"] == 60  # 10 + 20 + 30
        assert "hook_start" in packed_data["data"]
        assert "result_work" in packed_data["data"]
        assert "result_work_2" in packed_data["data"]
        assert packed_data["id"] == "test_detector"
    
    def test_manual_reset(self):
        """Test manual reset functionality"""
        # Partially complete pattern
        hook_au = self.create_mock_action_unit(action="start_work")
        self.detector.process_action_unit(hook_au)
        
        # Manual reset
        self.detector.reset()
        
        # Should be back to initial state but keep passed_au (current implementation)
        assert self.detector.currentState == BaseDetectorState.HOOK.value
        assert self.detector.currentIndex == 0
        # passed_au is not cleared in current reset implementation
        assert "hook_start" in self.detector.passed_au
    
    def test_signal_emission_timing(self):
        """Test that signals are emitted at correct times"""
        # Hook signal should be emitted after hook completion
        hook_au = self.create_mock_action_unit(action="start_work")
        self.detector.process_action_unit(hook_au)
        
        assert len(self.hook_signal_calls) == 1
        assert len(self.pattern_signal_calls) == 0
        
        # Pattern signal should be emitted after result completion
        result_au_1 = self.create_mock_action_unit(action_type="work")
        result_au_2 = self.create_mock_action_unit(action_type="work")
        
        self.detector.process_action_unit(result_au_1)
        assert len(self.pattern_signal_calls) == 0
        
        self.detector.process_action_unit(result_au_2)
        assert len(self.pattern_signal_calls) == 1