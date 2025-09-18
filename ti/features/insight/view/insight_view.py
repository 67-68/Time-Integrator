from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from ti.features.insight.view.insight_card import InsightCard


class InsightView(QScrollArea):
    """
    洞察视图 - 包含滚动区域的卡片容器
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setWidgetResizable(True)
        
        # 创建内容widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)
        
        # 设置滚动区域的内容
        self.setWidget(self.content_widget)
        
        # 存储卡片presenter引用
        self.card_presenters = {}
    
    def add_card(self, card: InsightCard):
        """
        把卡片加入scrolled area

        Args:
            card (InsightCard): 卡片widget
        """
        self.content_layout.addWidget(card)
    
    def clear_cards(self):
        """清空所有卡片"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.card_presenters.clear()