from dataclasses import dataclass
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.service.matchers import Matcher

@dataclass
class Monitor_Pack:
    """
    在调用monitor的时候用来规范数据形式
    """
    id: str  # detector recipe ID
    monitor_id: str  # monitor identifier
    hook: list[Matcher]
    
@dataclass
class Thread_Pack:
    monitors: dict[str,Monitor_Pack]
    thread_factory: 'DetectorFactory'
    thread_id: str