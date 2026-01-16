from datetime import datetime, timedelta


class DateUtils:
    """日期工具类，用于计算时间范围"""
    
    @staticmethod
    def get_date_range(days: int) -> tuple[str, str]:
        """
        获取过去N天的日期范围
        
        Args:
            days: 过去的天数
            
        Returns:
            tuple: (开始日期, 结束日期) 格式为 YYYY-MM-DD
        """
        end_date = datetime.now().date() - timedelta(days=1)  # 昨天
        start_date = end_date - timedelta(days=days - 1)
        
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_time_range_options() -> dict[str, int]:
        """
        获取时间范围选项
        
        Returns:
            dict: 选项名称到天数的映射
        """
        return {
            "过去一天": 1,
            "过去三天": 3,
            "过去一周": 7,
            "过去一个月": 30
        }
    
    @staticmethod
    def get_default_time_range() -> str:
        """获取默认时间范围选项"""
        return "过去一天"
    
    @staticmethod
    def format_date_range_display(start_date: str, end_date: str) -> str:
        """格式化日期范围显示"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start_date == end_date:
            return start_dt.strftime("%Y年%m月%d日")
        else:
            return f"{start_dt.strftime('%m月%d日')} - {end_dt.strftime('%m月%d日')}"