from PyQt6.QtCore import QObject, pyqtSignal
from ti.services.dataService import DataService
from ti.features.menu.service.time_analysis_service import TimeAnalysisService
from ti.features.menu.service.date_utils import DateUtils
from ti.features.menu.view.time_pie_chart import TimePieChart
from ti.model.action_unit import ActionUnit


class MenuPresenter(QObject):
    """
    Menu页面的Presenter
    负责获取数据、分析时间分配、更新视图
    """
    
    # 信号：当分析完成时发出
    analysis_completed = pyqtSignal(dict)
    
    def __init__(self, data_service: DataService):
        super().__init__()
        self.data_service = data_service
        self.analysis_service = TimeAnalysisService()
        self.pie_chart = None
        self.current_time_range = DateUtils.get_default_time_range()
    
    def set_pie_chart(self, pie_chart: TimePieChart):
        """设置饼图组件"""
        self.pie_chart = pie_chart
        
        # 为饼图添加默认分类
        category_matchers = self.analysis_service.get_category_matchers()
        for category_name, matcher in category_matchers.items():
            self.pie_chart.add_category(category_name, matcher)
        
        # 添加其他分类
        self.pie_chart.add_category("other", lambda au: True)  # 默认匹配所有
    
    def analyze_time(self, time_range_name: str = None):
        """分析指定时间范围的时间分配"""
        try:
            if time_range_name:
                self.current_time_range = time_range_name
            
            # 获取时间范围对应的天数
            time_range_options = DateUtils.get_time_range_options()
            days = time_range_options.get(self.current_time_range, 1)
            
            # 计算日期范围
            start_date, end_date = DateUtils.get_date_range(days)
            
            # 获取数据
            action_units = self.data_service.get_date_range_AU(start_date, end_date)
            
            if not action_units:
                print(f"没有找到{self.current_time_range}的数据")
                # 清空显示
                if self.pie_chart:
                    self.pie_chart.clear()
                    self.pie_chart.update_actions_list([])
                return
            
            # 分析时间分配
            analysis_result = self.analysis_service.analyze_time_distribution(
                action_units, self.current_time_range
            )
            
            # 分析前五行动
            top_actions = self.analysis_service.analyze_top_actions(action_units)
            
            # 更新饼图
            if self.pie_chart:
                self.pie_chart.add_time_from_action_units(action_units)
                # 更新行动列表
                self.pie_chart.update_actions_list(top_actions)
            
            # 发出分析完成信号
            self.analysis_completed.emit(analysis_result)
            
            # 打印摘要
            summary = self.analysis_service.get_summary_text(analysis_result)
            print(f"{self.current_time_range}时间分配分析结果:")
            print(summary)
            
            # 打印前五行动
            if top_actions:
                print(f"{self.current_time_range}时间花费前五的行动:")
                for i, (action_name, category, time_spent) in enumerate(top_actions, 1):
                    hours = time_spent / 60
                    print(f"{i}. {action_name} (类别: {category}, 时间: {hours:.1f}小时)")
            
        except Exception as e:
            print(f"分析时间时出错: {e}")
    
    def analyze_yesterday_time(self):
        """分析昨天的时间分配（向后兼容）"""
        self.analyze_time("过去一天")
    
    def refresh_data(self):
        """刷新数据"""
        self.analyze_time()
    
    def get_time_range_options(self) -> dict[str, int]:
        """获取时间范围选项"""
        return DateUtils.get_time_range_options()
    
    def set_time_range(self, time_range_name: str):
        """设置时间范围并重新分析"""
        self.analyze_time(time_range_name)
    
    def get_analysis_summary(self) -> str:
        """获取分析摘要文本"""
        try:
            yesterday_aus = self.data_service.get_yesterday_AU()
            if not yesterday_aus:
                return "暂无昨天数据"
            
            analysis_result = self.analysis_service.analyze_yesterday_time_distribution(yesterday_aus)
            return self.analysis_service.get_summary_text(analysis_result)
            
        except Exception as e:
            return f"获取分析摘要时出错: {e}"
    
    def add_custom_category(self, category_name: str, matcher):
        """
        添加自定义分类到分析服务和饼图
        
        Args:
            category_name: 分类名称
            matcher: 匹配函数
        """
        self.analysis_service.add_custom_category(category_name, matcher)
        if self.pie_chart:
            self.pie_chart.add_category(category_name, matcher)