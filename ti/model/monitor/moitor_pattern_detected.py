from dataclasses import dataclass
from typing import Protocol

from ti.core.Interfaces.basic_event import BasicEvent
from ti.features.detector.model.detectorFactory import DetectorFactory

@dataclass
class IMonitorEvent:
    thread_id: str
    monitor_id: str
    event_id: str = "monitor_event"

@dataclass
class MonitorPatternDetected:
    """
    monitor检测到状态之后发出的类

    Args:
        BasicEvent (_type_): _description_
    """
    thread_id: str
    monitor_id: str
    event_id: str = "monitor_pattern_detected"
    
    
    