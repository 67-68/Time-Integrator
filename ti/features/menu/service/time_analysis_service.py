from typing import List, Tuple
from ti.model.action_unit import ActionUnit
from ti.features.detector.service.matchers import Matcher
from ti.features.menu.service.date_utils import DateUtils


class TimeAnalysisService:
    """
    时间分析服务
    使用matchers来分类和分析时间分配
    """
    
    def __init__(self):
        self.matcher = Matcher()
        self.default_categories = {
            "waste": self.matcher.action_type_is("waste"),
            "work": self.matcher.action_type_is("work"), 
            "rest": self.matcher.action_type_is("rest")
        }
    
    def analyze_time_distribution(self, action_units: List[ActionUnit], time_range_name: str = "过去一天") -> dict:
        """
        分析指定时间范围内的时间分配
        
        Args:
            action_units: ActionUnit列表
            time_range_name: 时间范围名称
            
        Returns:
            dict: 包含各分类时间的字典
        """
        result = {}
        total_time = 0
        
        # 计算每个分类的时间
        for category_name, matcher in self.default_categories.items():
            category_time = self._calculate_category_time(action_units, matcher)
            result[category_name] = category_time
            total_time += category_time
        
        # 计算其他分类的时间
        other_time = 0
        for au in action_units:
            matched = False
            for matcher in self.default_categories.values():
                if matcher(au):
                    matched = True
                    break
            if not matched:
                other_time += au.timeSpan
        
        result["other"] = other_time
        total_time += other_time
        
        # 添加百分比信息
        result["total"] = total_time
        result["time_range"] = time_range_name
        
        for category in ["waste", "work", "rest", "other"]:
            if total_time > 0:
                result[f"{category}_percentage"] = (result[category] / total_time * 100)
            else:
                result[f"{category}_percentage"] = 0.0
        
        return result
    
    def analyze_yesterday_time_distribution(self, action_units: List[ActionUnit]) -> dict:
        """
        分析昨天的时间分配（向后兼容）
        
        Args:
            action_units: 昨天的ActionUnit列表
            
        Returns:
            dict: 包含各分类时间的字典
        """
        return self.analyze_time_distribution(action_units, "过去一天")
    
    def _calculate_category_time(self, action_units: List[ActionUnit], matcher) -> int:
        """
        计算特定分类的总时间
        
        Args:
            action_units: ActionUnit列表
            matcher: 匹配函数
            
        Returns:
            int: 总时间（分钟）
        """
        total_time = 0
        for au in action_units:
            if matcher(au):
                total_time += au.timeSpan
        return total_time
    
    def get_category_matchers(self) -> dict:
        """
        获取默认分类的matchers
        
        Returns:
            dict: 分类名称到matcher的映射
        """
        return self.default_categories.copy()
    
    def add_custom_category(self, category_name: str, matcher):
        """
        添加自定义分类
        
        Args:
            category_name: 分类名称
            matcher: 匹配函数
        """
        self.default_categories[category_name] = matcher
    
    def get_summary_text(self, analysis_result: dict) -> str:
        """
        生成时间分配的摘要文本
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            str: 摘要文本
        """
        total_hours = analysis_result["total"] / 60
        waste_percentage = analysis_result.get("waste_percentage", 0)
        work_percentage = analysis_result.get("work_percentage", 0)
        rest_percentage = analysis_result.get("rest_percentage", 0)
        time_range = analysis_result.get("time_range", "过去一天")
        
        summary = f"{time_range}总活动时间: {total_hours:.1f}小时\n"
        summary += f"工作: {work_percentage:.1f}%\n"
        summary += f"休息: {rest_percentage:.1f}%\n" 
        summary += f"浪费: {waste_percentage:.1f}%"
        
        return summary
    
    def analyze_top_actions(self, action_units: List[ActionUnit]) -> List[Tuple[str, str, int]]:
        """
        分析花费时间前五的行动
        
        Args:
            action_units: ActionUnit列表
            
        Returns:
            List[Tuple[str, str, int]]: 包含(行动名称, 类别, 时间)的元组列表
        """
        # 按行动名称和类别分组统计时间
        action_stats = {}
        
        for au in action_units:
            action_name = au.action
            # 确定类别
            category = "other"
            for cat_name, matcher in self.default_categories.items():
                if matcher(au):
                    category = cat_name
                    break
            
            # 关键：相同行动但不同类别视为不同的行动
            key = (action_name, category)
            if key not in action_stats:
                action_stats[key] = 0
            action_stats[key] += au.timeSpan
        
        # 按时间降序排序，取前五
        sorted_actions = sorted(action_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 转换为(行动名称, 类别, 时间)格式
        result = []
        for (action_name, category), time_spent in sorted_actions:
            result.append((action_name, category, time_spent))
        
        return result