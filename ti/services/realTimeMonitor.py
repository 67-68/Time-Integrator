from dataclasses import dataclass
from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.eventBus import EventBus
from PyQt6.QtCore import pyqtSignal, QObject

from ti.features.detector.model.baseDetector import BaseDetector
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.service.matchers import Matcher
from ti.services.dataService import DataService

@dataclass
class Monitor_Pack:
    id: str  # detector recipe ID
    monitor_id: str  # monitor identifier
    hook: list[Matcher]

@dataclass
class Thread_Pack:
    monitors: dict[str,Monitor_Pack]
    thread_factory: 'DetectorFactory'
    thread_id: str
    
    
class RealTimeMonitor(QObject):
    # App类传递信号
    intervention_needed = pyqtSignal()
    
    """_summary_
    它用来监控行为数据的输入
    如果特定的模式被触发
    那么上报Coodinator, 生成一个窗口
    使用线程概念来管理不同的监控任务
    """
    def __init__(
        self,
        DS: DataService, #用来检测信号发出
        bus: EventBus,
        parent = None
    ):
        super().__init__(parent)
        
        # 线程管理
        self.threads: dict[str, Thread_Pack] = {}
        self.bus = bus
        
        # 连接信号
        DS.actionUnit_added.connect(lambda au: self._on_action_recorded(au))
    
    def create_thread(self, thread_id: str, detector_factory: DetectorFactory) -> str:
        """
        创建一个新的监控线程
        
        Args:
            thread_id (str): 线程ID
            detector_factory (DetectorFactory): 该线程使用的detector工厂
            
        Returns:
            str: 创建的线程ID
        """
        if thread_id in self.threads:
            raise ValueError(f"Thread with ID '{thread_id}' already exists")
        
        thread_pack = Thread_Pack(
            monitors={},
            thread_factory=detector_factory,
            thread_id=thread_id
        )
        
        self.threads[thread_id] = thread_pack
        print(f"[RealTimeMonitor] Created thread: {thread_id}")
        return thread_id
    
    def add_monitor_to_thread(
        self,
        thread_id: str,
        monitor_pack: Monitor_Pack
    ):
        """
        向指定线程添加监控项目
        
        Args:
            thread_id (str): 线程ID
            monitor_pack (Monitor_Pack): 监控项目包
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread with ID '{thread_id}' does not exist")
        
        thread_pack = self.threads[thread_id]
        detector_id = monitor_pack.id  # detector recipe ID
        monitor_id = monitor_pack.monitor_id  # monitor identifier
        
        # 使用线程的detector factory创建detector
        detector = thread_pack.thread_factory.create_detector(detector_id)
        
        # 连接信号
        detector.hook_pattern_detected.connect(
            lambda detector_data, current_id=monitor_id, t_id=thread_id: 
            self._on_pattern_detected(current_id, t_id)
        )
        
        # 存储监控项目
        thread_pack.monitors[monitor_id] = (monitor_pack, detector)
        print(f"[RealTimeMonitor] Added monitor '{detector_id}' to thread '{thread_id}'")
    
    def remove_monitor_from_thread(self, thread_id: str, monitor_id: str):
        """
        从指定线程移除监控项目
        
        Args:
            thread_id (str): 线程ID
            monitor_id (str): 监控项目ID
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread with ID '{thread_id}' does not exist")
        
        thread_pack = self.threads[thread_id]
        if monitor_id in thread_pack.monitors:
            del thread_pack.monitors[monitor_id]
            print(f"[RealTimeMonitor] Removed monitor '{monitor_id}' from thread '{thread_id}'")
    
    def remove_thread(self, thread_id: str):
        """
        移除整个线程
        
        Args:
            thread_id (str): 线程ID
        """
        if thread_id in self.threads:
            del self.threads[thread_id]
            print(f"[RealTimeMonitor] Removed thread: {thread_id}")
    
    def get_thread(self, thread_id: str) -> Thread_Pack:
        """
        获取指定线程
        
        Args:
            thread_id (str): 线程ID
            
        Returns:
            Thread_Pack: 线程包
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread with ID '{thread_id}' does not exist")
        
        return self.threads[thread_id]
    
    def list_threads(self) -> list[str]:
        """
        获取所有线程ID列表
        
        Returns:
            list[str]: 线程ID列表
        """
        return list(self.threads.keys())
    
    def list_monitors_in_thread(self, thread_id: str) -> list[str]:
        """
        获取指定线程中的所有监控项目ID
        
        Args:
            thread_id (str): 线程ID
            
        Returns:
            list[str]: 监控项目ID列表
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread with ID '{thread_id}' does not exist")
        
        return list(self.threads[thread_id].monitors.keys())
    
    def _on_action_recorded(self, au):
        """
        处理行动单元记录事件
        在所有线程的所有监控项目中处理行动单元
        """
        for thread_id, thread_pack in self.threads.items():
            for monitor_id, (monitor_pack, detector) in thread_pack.monitors.items():
                detector: BaseDetector
                detector.process_action_unit(au)
                action = au.action  # 现在使用 ActionUnit 对象的属性而不是字典访问
                print(f"[Thread {thread_id}] 正在判断行动为{action}的行动单元")
    
    def _on_pattern_detected(self, monitor_id: str, thread_id: str):
        """
        处理模式检测事件
        
        Args:
            monitor_id (str): 监控项目ID
            thread_id (str): 线程ID
        """
        print(f"[Thread {thread_id}] monitor检测到模式id为{monitor_id}的模式匹配")
        signal_name = f"{thread_id}_{monitor_id}_pattern_detected"
        self.bus.publish(signal_name, (thread_id, monitor_id)) # 这里应该发布对应的行动
        print(f"发布了信号名称为{signal_name}的信号")
        self.intervention_needed.emit()
        
        
