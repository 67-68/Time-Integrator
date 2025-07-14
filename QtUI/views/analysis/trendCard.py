from Core.utils import load_svg_icon
from QtUI.rawUI.ui_rawDailyTrendCard import Ui_trendCard
from QtUI.widgets.pages.BasicWidget import BasicWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor

class TrendCard(BasicWidget):
    def __init__(self,data,parent = None):
        super().__init__(parent)
        
        self.TC = Ui_trendCard()
        self.TC.setupUi(self)
        
        pre = data["presentation"]
        
        #这里手动填充各项数据
        sementic = data["text"]["sementic"]
        judgements = data["text"]["judgement"]
        title = pre["title"]
        color = pre["color"]
        
        # --- 这是新的、正确的方式来设置图标 ---
        icon_path = data["presentation"]["icon"]
        icon_color_str = data["presentation"]["color"] # e.g., "#3498DB"
        
        # 将颜色字符串转换为QColor对象
        icon_color = QColor(icon_color_str)
        
        # 定义你想要的图标尺寸
        icon_size = QSize(48, 48) 
        
        # 使用我们的工具函数加载、渲染并着色SVG
        icon_pixmap = load_svg_icon(icon_path, icon_size, icon_color)
        
        # 将最终的位图设置给QLabel
        self.TC.iconLabel.setPixmap(icon_pixmap)
        self.TC.iconLabel.setFixedSize(icon_size) # 最好固定尺寸，防止布局变化
        
        self.TC.sementicLabel.setText(sementic)
        
        judgements_text = ""
        for judgement in judgements:
            judgements_text = judgements_text + judgement + "\n"
            
        self.TC.judgementLabel.setText(judgements_text)
        
        self.TC.titleLabel.setText(title)
        
        
        
        
        
        