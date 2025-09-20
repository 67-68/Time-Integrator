
from ti.core.Interfaces.basic_event import BasicEvent


class CaptureSaveRecord(BasicEvent):
    event_id: str
    
class CaptureNewRecord(BasicEvent):
    pass

class CaptureRecordDelete(BasicEvent):
    pass