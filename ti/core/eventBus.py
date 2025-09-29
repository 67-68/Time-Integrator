from dataclasses import dataclass

from ti.core.Interfaces.basic_event import BasicEvent


class EventBus:
    def __init__(self):
        """_summary_
        这个类扮演类似基础设施的角色
        它把一个信息从一个类传送给其他类
        """
        self.signals = {}
        self.event_signals = {}
    
    def subscribe(self,signal_id: str,func):
        """_summary_
        这个函数允许类订阅某个信号
        在信号激活后，会自动把信息送给订阅者
        Args:
            signal_id(str): 希望订阅信号的名称
            func (function): 回调函数，在这里放上希望接受信号之后激活的函数
        """
        if signal_id not in self.signals:
            self.signals[signal_id] = []
            
        self.signals[signal_id].append(func)
        print(f"[BUS]subscribed {signal_id}")
    
    def publish(self,signal_id,data):
        """_summary_
        这个函数允许类发布某个信号
        在信号激活后，会自动把信息送给订阅者
        Args:
            signal_id(str): 希望发布信号的名称
            data (dict): 希望发布的信息
        """
        if signal_id not in self.signals:
            self.signals[signal_id] = []
            print(f"this signal({signal_id}) is not registed by subscriber or publisher")
        
        signal_list = self.signals[signal_id]
        print(f"[BUS]published {signal_id}")
        
        if len(signal_list) == 0:
            return
        
        for func in signal_list:
            func(data)
    
    def subscribe_event(self,event: type[BasicEvent],func):
        """_summary_
        这个函数允许类订阅某个信号
        在信号激活后，会自动把信息送给订阅者
        Args:
            signal_id(str): 希望订阅信号的名称
            func (function): 回调函数，在这里放上希望接受信号之后激活的函数
        """
        signal_id = event.event_id
        if event not in self.event_signals:
            self.event_signals[signal_id] = []
            
        self.event_signals[signal_id].append(func)
        print(f"[BUS]subscribed {signal_id}")
    
    def publish_event(self,event: type[BasicEvent],data):
        """_summary_
        这个函数允许类发布某个信号
        在信号激活后，会自动把信息送给订阅者
        Args:
            signal_id(str): 希望发布信号的名称
            data (dict): 希望发布的信息
        """
        if event not in self.event_signals:
            self.event_signals[event] = []
            print(f"this signal({event.event_id}) is not registed by subscriber or publisher")
            
        signal_list = self.event_signals[event]
        print(f"[BUS]published {event.event_id}")
        if len(signal_list) == 0:
            return
        
        for func in signal_list:
            func(data)
    
        
        