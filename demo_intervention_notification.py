#!/usr/bin/env python3
"""
演示干预通知功能 - 弹窗方案
"""

import sys
import time
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication

# 添加项目路径
sys.path.insert(0, '/Users/lennon/Projects/Time_Integrater')

from ti.features.intervention.presenter.intervention_presenter import InterventionPresenter
from ti.features.intervention.model.stored.inv_real_time_annoying import RealTimeAnnoying

def demo_tkinter_notification():
    """演示tkinter弹窗通知"""
    print("=== 演示tkinter弹窗通知 ===")
    print("这个演示会显示一个模态弹窗，用户必须手动关闭")
    print("弹窗会显示50秒（每10秒显示一次，共5次）")
    print()
    
    # 创建测试数据（立即开始）
    test_data = RealTimeAnnoying(
        action_name="学习Python",
        action_detail="完成第5章练习",
        start_time=datetime.now()
    )
    
    # 创建Presenter
    presenter = InterventionPresenter()
    
    # 注册干预
    presenter.register_intervention(test_data)
    
    print("干预已注册，开始演示通知...")
    print("注意：弹窗会阻塞程序执行，直到用户关闭")
    print()
    
    # 手动触发干预（模拟定时器触发）
    presenter.intervene_user()
    
    print("第一个通知已显示，等待用户关闭...")
    print("后续通知会每10秒自动显示")
    print()
    
    # 等待一段时间让用户看到效果
    print("等待30秒观察通知行为...")
    time.sleep(30)
    
    # 停止干预
    presenter.stop_intervention()
    print("干预已停止")
    
    # 关闭Presenter
    presenter.shutdown()

def demo_pync_fallback():
    """演示pync回退方案"""
    print("\n=== 演示pync回退方案 ===")
    print("这个演示会测试tkinter不可用时回退到pync")
    print()
    
    # 创建测试数据
    test_data = RealTimeAnnoying(
        action_name="锻炼",
        action_detail="跑步30分钟",
        start_time=datetime.now()
    )
    
    # 创建Presenter
    presenter = InterventionPresenter()
    
    # 注册干预
    presenter.register_intervention(test_data)
    
    print("干预已注册，测试pync回退...")
    print("注意：如果tkinter可用，会优先使用tkinter")
    print()
    
    # 直接测试回退方法
    presenter._send_pync_notification()
    
    print("pync通知已发送（如果pync可用）")
    
    # 停止干预
    presenter.stop_intervention()
    print("干预已停止")
    
    # 关闭Presenter
    presenter.shutdown()

def main():
    """主演示函数"""
    print("干预通知功能演示")
    print("=" * 50)
    
    # 需要QApplication实例
    app = QApplication([])
    
    try:
        # 演示tkinter弹窗
        demo_tkinter_notification()
        
        # 演示pync回退
        demo_pync_fallback()
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
    
    print("\n演示完成！")
    print("新的弹窗方案特点：")
    print("- 使用tkinter模态弹窗，用户必须手动关闭")
    print("- 每10秒显示一次通知，持续50秒")
    print("- 如果tkinter不可用，回退到pync通知")
    print("- 每次通知都播放系统提示音")

if __name__ == "__main__":
    main()