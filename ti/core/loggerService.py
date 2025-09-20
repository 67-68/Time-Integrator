import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class LoggerService:
    """
    日志服务，用于按功能模块记录日志到JSON文件
    """
    
    def __init__(self, feature_base_dir: str, feature_name: str):
        """
        初始化日志服务
        
        Args:
            feature_base_dir: 功能模块的基础目录路径
            feature_name: 功能模块名称
        """
        self.feature_base_dir = feature_base_dir
        self.feature_name = feature_name
        self.log_file_path = Path(feature_base_dir) / f"{feature_name}_log.json"
        self.logs: List[Dict[str, str]] = []
        
        # 确保目录存在
        os.makedirs(feature_base_dir, exist_ok=True)
        
        # 加载现有日志或创建新文件
        self._load_logs()
    
    def _load_logs(self):
        """加载现有日志文件，如果不存在则创建空列表"""
        if self.log_file_path.exists():
            try:
                with open(self.log_file_path, 'r', encoding='utf-8') as f:
                    self.logs = json.load(f)
                # 确保logs是列表类型
                if not isinstance(self.logs, list):
                    self.logs = []
            except (json.JSONDecodeError, FileNotFoundError):
                self.logs = []
        else:
            self.logs = []
    
    def _save_logs(self):
        """保存日志到文件"""
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
    
    def log(self, topic: str, content: str):
        """
        记录日志
        
        Args:
            topic: 日志主题
            content: 日志内容
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "content": content
        }
        
        self.logs.append(log_entry)
        self._save_logs()
    
    def get_logs(self) -> List[Dict[str, str]]:
        """
        获取所有日志记录
        
        Returns:
            所有日志记录的列表
        """
        return self.logs.copy()
    
    def clear_logs(self):
        """清空所有日志记录"""
        self.logs = []
        self._save_logs()
    
    def get_recent_logs(self, count: int = 10) -> List[Dict[str, str]]:
        """
        获取最近的日志记录
        
        Args:
            count: 要获取的日志数量
            
        Returns:
            最近的日志记录列表
        """
        return self.logs[-count:] if self.logs else []