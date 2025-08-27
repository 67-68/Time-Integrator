
from ti.dataAccess.dataService import DataService
from PyQt6.QtCore import pyqtSignal,QObject

from ti.domain.detector.baseDetector import BaseDetector
from ti.domain.detector.detectorFactory import DetectorFactory



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
        parent = None
    ):
        super().__init__(parent)
        
        # 用来存储每个需要Monitor的Intervention的Detector和卡片ui
        self.monitor_projects = {} #按理来说应该包含Detector key和id 和
        self.DF = DF
        
        # 连接信号
        DS.actionUnit_added.connect(lambda au: self._on_action_recorded(au))
        
    
    def add_monitor_project(self,monitor_pack):
        # 按理来说, Monitor_pack 应该包含detector和id和ui
        
        ui = monitor_pack["ui"]
        id = monitor_pack["id"]
        
        detector= self.DF.create_detector(id,id)
        
        
        detector.pattern_detected.connect(lambda f: self._on_pattern_detected(f))
        
        self.monitor_projects[id] = monitor_pack
        
    def _on_action_recorded(self,au):
        # 过一遍所有Detector
        for id in self.monitor_projects:
            detector:BaseDetector = self.monitor_projects[id]["detector"]
            detector.process_action_unit(au)
            
            print(au)
            
    def _on_pattern_detected(self, ui):
        # 汇报Coodinator. app
        self.intervention_needed.emit(ui)
        