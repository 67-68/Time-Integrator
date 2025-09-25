from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from typing import Dict, Callable, List, Tuple
from ti.model.action_unit import ActionUnit

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['STHeiti', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class TimePieChart(QWidget):
    """
    时间分配饼图组件
    使用matchers来动态添加时间分类，基于matplotlib
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.total_time = 0
        self.category_data: Dict[str, int] = {}
        self.category_matchers: Dict[str, Callable[[ActionUnit], bool]] = {}
        self.time_range_changed_callback = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        
        # 标题和时间选择器行
        header_layout = QHBoxLayout()
        
        # 标题
        self.title_label = QLabel("时间分配分析")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # 时间范围选择器
        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems(["过去一天", "过去三天", "过去一周", "过去一个月"])
        self.time_range_combo.setCurrentText("过去一天")
        self.time_range_combo.currentTextChanged.connect(self._on_time_range_changed)
        self.time_range_combo.setStyleSheet("""
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 100px;
            }
        """)
        header_layout.addWidget(self.time_range_combo)
        
        layout.addLayout(header_layout)
        
        # 主要内容区域（饼图 + 行动列表）
        content_layout = QHBoxLayout()
        
        # 左侧：饼图区域
        chart_layout = QVBoxLayout()
        
        # 饼图画布
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        
        # 总计标签
        self.total_label = QLabel("总时间: 0分钟")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_layout.addWidget(self.total_label)
        
        content_layout.addLayout(chart_layout)
        
        # 右侧：行动列表区域
        actions_layout = QVBoxLayout()
        
        # 行动列表标题
        actions_title = QLabel("时间花费前五的行动")
        actions_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 8px;")
        actions_layout.addWidget(actions_title)
        
        # 行动列表
        self.actions_list = QListWidget()
        self.actions_list.setMaximumWidth(300)
        self.actions_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        actions_layout.addWidget(self.actions_list)
        
        content_layout.addLayout(actions_layout)
        
        layout.addLayout(content_layout)
    
    def add_category(self, category_name: str, matcher: Callable[[ActionUnit], bool]):
        """
        添加一个时间分类
        
        Args:
            category_name: 分类名称
            matcher: 匹配函数，接受ActionUnit返回bool
        """
        self.category_matchers[category_name] = matcher
        self.category_data[category_name] = 0
    
    def add_time_from_action_units(self, action_units: list[ActionUnit]):
        """
        从ActionUnit列表添加时间到饼图
        
        Args:
            action_units: ActionUnit列表
        """
        # 重置数据
        self.total_time = 0
        for category in self.category_data:
            self.category_data[category] = 0
        
        # 计算每个分类的时间
        for au in action_units:
            for category_name, matcher in self.category_matchers.items():
                if matcher(au):
                    self.category_data[category_name] += au.timeSpan
                    self.total_time += au.timeSpan
                    break  # 一个AU只属于一个分类
        
        self.update_chart()
    
    def update_chart(self):
        """更新饼图显示"""
        # 清除现有图表
        self.figure.clear()
        
        # 准备数据
        labels = []
        sizes = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
        
        for category_name, time in self.category_data.items():
            if time > 0:
                labels.append(category_name)
                sizes.append(time)
        
        if not sizes:  # 如果没有数据
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # 创建饼图
            ax = self.figure.add_subplot(111)
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                colors=colors[:len(sizes)],
                startangle=90
            )
            
            # 设置样式
            ax.set_title('时间分配', fontsize=14, fontweight='bold')
            
            # 美化百分比文本
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        # 更新画布
        self.canvas.draw()
        
        # 更新总计
        self.total_label.setText(f"总时间: {self.total_time}分钟 ({self.total_time/60:.1f}小时)")
    
    def update_actions_list(self, top_actions: List[Tuple[str, str, int]]):
        """
        更新行动列表显示
        
        Args:
            top_actions: 包含(行动名称, 类别, 时间)的元组列表
        """
        self.actions_list.clear()
        
        if not top_actions:
            item = QListWidgetItem("暂无数据")
            self.actions_list.addItem(item)
            return
        
        for i, (action_name, category, time_spent) in enumerate(top_actions, 1):
            hours = time_spent / 60
            item_text = f"{i}. {action_name}\n   类别: {category}, 时间: {hours:.1f}小时"
            item = QListWidgetItem(item_text)
            self.actions_list.addItem(item)
    
    def set_time_range_changed_callback(self, callback):
        """设置时间范围改变的回调函数"""
        self.time_range_changed_callback = callback
    
    def _on_time_range_changed(self, time_range_name):
        """时间范围改变时的处理"""
        if self.time_range_changed_callback:
            self.time_range_changed_callback(time_range_name)
    
    def set_time_range(self, time_range_name):
        """设置时间范围"""
        self.time_range_combo.setCurrentText(time_range_name)
    
    def clear(self):
        """清空饼图数据"""
        self.total_time = 0
        self.category_data = {name: 0 for name in self.category_matchers.keys()}
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', fontsize=16)
        ax.axis('off')
        self.canvas.draw()
        self.total_label.setText("总时间: 0分钟")