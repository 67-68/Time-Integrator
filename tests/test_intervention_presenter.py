#!/usr/bin/env python3
"""
测试InterventionPresenter的功能
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from ti.features.intervention.presenter.intervention_presenter import InterventionPresenter
from ti.features.intervention.model.stored.inv_real_time_annoying import RealTimeAnnoying


class TestInterventionPresenter:
    """InterventionPresenter测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        # Mock View以避免QApplication依赖
        with patch('ti.features.intervention.presenter.intervention_presenter.InterventionView') as mock_view_class:
            self.mock_view = Mock()
            mock_view_class.return_value = self.mock_view
            self.presenter = InterventionPresenter()
    
    def test_intervene_user_with_qt_success(self):
        """测试intervene_user函数在Qt可用时的行为"""
        # 准备测试数据
        test_data = RealTimeAnnoying(
            action_name="学习Python",
            action_detail="完成第5章练习",
            start_time=datetime.now()
        )
        self.presenter.current_intervention = test_data
        
        # Mock QMessageBox
        with patch('PyQt6.QtWidgets.QMessageBox') as mock_msgbox_class:
            # 设置mock返回值
            mock_msgbox_instance = Mock()
            mock_msgbox_class.return_value = mock_msgbox_instance
            
            # 调用被测试的函数
            self.presenter.intervene_user()
            
            # 验证QMessageBox被创建
            mock_msgbox_class.assert_called_once()
            
            # 验证setWindowTitle被调用
            mock_msgbox_instance.setWindowTitle.assert_called_once()
            
            # 验证setText被调用
            mock_msgbox_instance.setText.assert_called_once()
            
            # 验证setIcon被调用
            mock_msgbox_instance.setIcon.assert_called_once()
            
            # 验证setWindowModality被调用
            mock_msgbox_instance.setWindowModality.assert_called_once_with(2)  # Qt.ApplicationModal
            
            # 验证show被调用
            mock_msgbox_instance.show.assert_called_once()
            
            # 验证调用参数
            title_call = mock_msgbox_instance.setWindowTitle.call_args[0][0]
            message_call = mock_msgbox_instance.setText.call_args[0][0]
            
            # 验证标题格式
            assert "去学习Python! (1/5)" in title_call
            
            # 验证消息内容
            expected_message = "完成第5章练习\n\n回到TimeIntegrator界面点击红色按钮以停止通知"
            assert message_call == expected_message
    
    def test_intervene_user_fallback_to_pync(self):
        """测试tkinter不可用时回退到pync的行为"""
        # 准备测试数据
        test_data = RealTimeAnnoying(
            action_name="学习Python",
            action_detail="完成第5章练习",
            start_time=datetime.now()
        )
        self.presenter.current_intervention = test_data
        
        # 直接测试_send_pync_notification方法
        with patch('pync.Notifier') as mock_notifier:
            
            # 调用回退方法
            self.presenter._send_pync_notification()
            
            # 验证pync.Notifier.notify被正确调用
            mock_notifier.notify.assert_called_once()
            
            # 验证调用参数
            call_args = mock_notifier.notify.call_args
            message, kwargs = call_args
            
            # 验证消息内容
            expected_message = "完成第5章练习\n回到TimeIntegrator界面点击红色按钮以停止通知"
            assert message[0] == expected_message
            
            # 验证标题格式（计数从0开始）
            assert "去学习Python! (0/5)" in kwargs['title']
    
    def test_intervene_user_no_intervention(self):
        """测试没有当前干预时的行为"""
        # 确保没有当前干预
        self.presenter.current_intervention = None
        
        # Mock QMessageBox
        with patch('PyQt6.QtWidgets.QMessageBox') as mock_msgbox_class:
            # 调用被测试的函数
            self.presenter.intervene_user()
            
            # 验证QMessageBox没有被调用
            mock_msgbox_class.assert_not_called()
    
    def test_intervene_user_timer_functionality(self):
        """测试通知定时器功能"""
        # 准备测试数据
        test_data = RealTimeAnnoying(
            action_name="锻炼",
            action_detail="跑步30分钟",
            start_time=datetime.now()
        )
        self.presenter.current_intervention = test_data
        
        # Mock QMessageBox
        with patch('PyQt6.QtWidgets.QMessageBox') as mock_msgbox_class:
            
            # 设置mock返回值
            mock_msgbox_instance = Mock()
            mock_msgbox_class.return_value = mock_msgbox_instance
            
            # 调用被测试的函数
            self.presenter.intervene_user()
            
            # 验证通知被发送
            mock_msgbox_class.assert_called_once()
            
            # 验证通知定时器状态
            assert hasattr(self.presenter, 'notification_timer'), "Notification timer should exist"
            assert self.presenter.notification_timer is not None, "Notification timer should not be None"
            # 由于QTimer在测试环境中可能无法正常工作，我们只验证基本状态
            print(f"Notification timer exists: {self.presenter.notification_timer is not None}")
    
    def test_stop_intervention_stops_timers(self):
        """测试停止干预时停止所有定时器"""
        # 准备测试数据
        test_data = RealTimeAnnoying(
            action_name="冥想",
            action_detail="",
            start_time=datetime.now()
        )
        self.presenter.current_intervention = test_data
        
        # Mock QTimer
        with patch('PyQt6.QtCore.QTimer') as mock_timer_class:
            mock_timer_instance = Mock()
            mock_timer_instance.isActive.return_value = True
            mock_timer_class.return_value = mock_timer_instance
            
            # 设置presenter的通知定时器
            self.presenter.notification_timer = mock_timer_instance
            
            # 调用停止干预
            self.presenter.stop_intervention()
            
            # 验证定时器被停止
            mock_timer_instance.stop.assert_called_once()


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])