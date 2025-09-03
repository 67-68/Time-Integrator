
from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.definitions import Monitor_Pack
from ti.core.eventBus import EventBus
from PyQt6.QtCore import pyqtSignal,QObject

from ti.features.detector.baseDetector import BaseDetector
from ti.features.detector.detectorFactory import DetectorFactory
from ti.services.dataAccess.dataService import DataService






class RealTimeMonitor(QObject):
    # App类传递信号
    intervention_needed = pyqtSignal()
    
    """_summary_
    它用来监控行为数据的输入
    如果特定的模式被触发
    那么上报Coodinator, 生成一个窗口
    """
    def __init__(
        self,
        DS: DataService, #用来检测信号发出
        DF: DetectorFactory,
        bus: EventBus,
        parent = None
    ):
        super().__init__(parent)
        
        # 用来存储每个需要Monitor的Intervention的Detector和卡片ui
        self.monitor_projects = {} #按理来说应该包含Detector key和id 和
        self.DF = DF
        self.bus = bus
        
        # 连接信号
        DS.actionUnit_added.connect(lambda au: self._on_action_recorded(au))
        
    
    def add_monitor_project(
        self,
        monitor_pack: Monitor_Pack
    ):
        # 按理来说, Monitor_pack 应该包含detector和id和ui
        
        id = monitor_pack.id
        hook = monitor_pack.hook
        
        detector = self.DF.create_detector(id,id) #Monitor 逻辑出问题了。直接使用hook
        
        detector.hook_pattern_detected.connect(lambda detector_data, current_id = id: self._on_pattern_detected(current_id)) # 应该是它自己也有传送东西,加上一个参数就行了
        
        self.monitor_projects[id] = (monitor_pack,detector)
        
    def _on_action_recorded(self,au):
        # 过一遍所有Detector
        for id in self.monitor_projects:
            Monitor_Pack,detector = self.monitor_projects[id]
            detector: type[BaseDetector]
            detector.process_action_unit(au)
            action = au["action"]
            print(f"正在判断行动为{action}的行动单元")
            
    def _on_pattern_detected(self,current_id):
        # 汇报Coodinator. app
        print(f"monitor检测到模式id为{current_id}的模式匹配")
        signal_name = f"{current_id}_pattern_detected"
        self.bus.publish(signal_name,current_id)
        print(f"发布了信号名称为{signal_name}的信号")
        self.intervention_needed.emit()
        
        