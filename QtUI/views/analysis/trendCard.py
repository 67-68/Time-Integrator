from QtUI.rawUI.ui_rawDailyTrendCard import Ui_trendCard
from QtUI.widgets.pages.BasicWidget import BasicWidget

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
        icon = pre["icon"]
        color = pre["color"]
        
        self.TC.sementicLabel.setText(sementic)
        
        judgements_text = ""
        for judgement in judgements:
            judgements_text = judgements_text + judgement + "\n"
        self.TC.judgementLabel.setText(judgements_text)
        
        self.TC.titleLabel.setText(title)
        
        self.TC.iconLabel.setText(icon)
        
        
        
        
        
        