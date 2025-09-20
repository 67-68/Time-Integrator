#!/usr/bin/env python3
"""
LoggerService使用示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ti.services.serviceContainer import ServiceContainer

def example_usage():
    # 创建服务容器
    service_container = ServiceContainer()
    
    # 创建logger service实例
    logger = service_container.create_logger_service(
        feature_base_dir="./ti/features/capture",
        feature_name="capture"
    )
    
    # 记录一些日志
    logger.log("启动", "捕获功能模块启动")
    logger.log("操作", "用户开始输入行动单元")
    logger.log("完成", "行动单元保存成功")
    
    # 获取并打印日志
    logs = logger.get_logs()
    print("记录的所有日志:")
    for log in logs:
        print(f"{log['timestamp']} - {log['topic']}: {log['content']}")

if __name__ == "__main__":
    example_usage()