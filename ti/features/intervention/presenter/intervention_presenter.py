import os
import platform
from datetime import datetime
from PyQt6.QtCore import QTimer
from ti.features.intervention.presenter.IIntervention_presenter import IInterventionPresenter
from ti.features.intervention.model.stored.inv_real_time_annoying import RealTimeAnnoying
from ti.features.intervention.view.intervention_view import InterventionView


class InterventionPresenter(IInterventionPresenter):
    """
    创建并掌控interventionView
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_intervention: RealTimeAnnoying | None = None
        self.view = InterventionView()
        self.notification_timer: QTimer | None = None
        self.notification_count = 0
        self._connect_signals()
        self._setup_timer()
        self._setup_notification_timer()
    
    def _connect_signals(self):
        print("Connecting signals...")
        self.view.intervention_saved.connect(self.register_intervention)
        self.view.stop_requested.connect(self.stop_intervention)
        print("Signals connected successfully")
    
    def _setup_timer(self):
        """设置每分钟调用run_life_cycle的定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_life_cycle)
        self.timer.start(60 * 1000)  # 60秒 = 60000毫秒
        print("Timer started - will check interventions every minute")
    
    def _setup_notification_timer(self):
        """设置通知定时器（用于重复通知）"""
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self._send_notification)
        # 初始不启动，只在需要时启动
        print("Notification timer created (not started)")
    
    def _play_system_sound(self):
        """播放系统提示音"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                # 使用afplay播放系统声音
                os.system("afplay /System/Library/Sounds/Ping.aiff &")
            print("System sound played")
        except Exception as e:
            print(f"Failed to play system sound: {e}")
    
    def register_intervention(self, data: RealTimeAnnoying):
        """
        登记Intervention
        目前仅支持登记一个
        如果发现已经有一个在类变量那么print
        """
        if self.current_intervention is not None:
            print("Warning: Already have an intervention registered")
            self.view.update_status("警告：已有一个干预在运行中")
        else:
            self.current_intervention = data
            print(f"Registered intervention: {data.action_name}")
            self.view.update_status(f"✓ 已设置干预：{data.action_name}")
    
    def is_pass_due(self):
        """
        根据开始时间和当前时间检验是否需要开始响铃
        如果需要，输出True
        """
        if self.current_intervention is None:
            return False
        
        current_time = datetime.now()
        return current_time >= self.current_intervention.start_time
    
    def intervene_user(self):
        """
        使用弹窗干扰用户
        显示Detail以及让她回到界面点击停止
        """
        if self.current_intervention is None:
            return
        print("try intervene...")
        
        # 启动重复通知定时器
        self._start_notification_cycle()
        
        # 立即发送第一个通知
        self._send_notification()
    
    def _start_notification_cycle(self):
        """开始重复通知周期"""
        if self.notification_timer and not self.notification_timer.isActive():
            self.notification_count = 0
            # 每10秒发送一次通知，持续50秒（共5次）
            self.notification_timer.start(10 * 1000)  # 10秒间隔
            print("Notification cycle started (10 second intervals)")
    
    def _stop_notification_cycle(self):
        """停止重复通知周期"""
        if self.notification_timer and self.notification_timer.isActive():
            self.notification_timer.stop()
            self.notification_count = 0
            print("Notification cycle stopped")
    
    def _send_notification(self):
        """发送单个通知"""
        if self.current_intervention is None:
            self._stop_notification_cycle()
            return
        
        self.notification_count += 1
        
        # 最多发送5次通知（50秒）
        if self.notification_count > 5:
            self._stop_notification_cycle()
            return
        
        try:
            # 使用Qt的QMessageBox替代tkinter
            from PyQt6.QtWidgets import QMessageBox
            
            # 创建消息框
            title = f"去{self.current_intervention.action_name}! ({self.notification_count}/5)"
            message = f"{self.current_intervention.action_detail}\n\n回到TimeIntegrator界面点击红色按钮以停止通知"
            
            # 显示模态消息框（用户必须手动关闭）
            msg_box = QMessageBox()
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Icon.Information)
            
            # 设置消息框为应用程序模态
            msg_box.setWindowModality(2)  # Qt.ApplicationModal
            
            # 显示消息框（非阻塞方式，使用exec()会阻塞）
            msg_box.show()
            
            # 播放系统提示音
            self._play_system_sound()
            
            print(f"Qt notification {self.notification_count}/5 sent and displayed")
            
        except Exception as e:
            print(f"Failed to send Qt notification: {e}")
            # 回退到pync
            self._send_pync_notification()
    
    def _send_pync_notification(self):
        """使用pync发送通知（回退方案）"""
        try:
            from pync import Notifier
            title = f"去{self.current_intervention.action_name}! ({self.notification_count}/5)"
            message = f"{self.current_intervention.action_detail}\n回到TimeIntegrator界面点击红色按钮以停止通知"
            
            Notifier.notify(message, title=title, sound="Ping")
            
            # 播放系统提示音
            self._play_system_sound()
            
            print(f"Pync notification {self.notification_count}/5 sent")
            
        except ImportError:
            print(f"INTERVENTION: {self.current_intervention.action_name} ({self.notification_count}/5)")
            print(f"Detail: {self.current_intervention.action_detail}")
            print("Please return to the interface and click stop!")
            # 即使pync不可用也尝试播放系统声音
            self._play_system_sound()
    
    def stop_intervention(self):
        """
        清空当前action缓存
        """
        # 停止通知定时器
        self._stop_notification_cycle()
        
        if self.current_intervention is not None:
            print(f"Stopped intervention: {self.current_intervention.action_name}")
            self.view.update_status(f"✓ 已停止干预：{self.current_intervention.action_name}")
            self.current_intervention = None
        else:
            self.view.update_status("没有正在运行的干预")
    
    def run_life_cycle(self):
        """
        检验所有Intervention
        调用is_pass_due
        如果True，调用
        """
        print(f"[Timer] Checking interventions at {datetime.now().strftime('%H:%M:%S')}")
        if self.is_pass_due():
            print("[Timer] Intervention is due - calling intervene_user")
            self.intervene_user()
        else:
            print("[Timer] No intervention due")
    
    def initialize(self):
        return super().initialize()
    
    def shutdown(self):
        """关闭Presenter，清理资源"""
        # 停止所有定时器
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            print("Intervention timer stopped")
        
        if hasattr(self, 'notification_timer') and self.notification_timer and self.notification_timer.isActive():
            self.notification_timer.stop()
            print("Notification timer stopped")
            
        return super().shutdown()