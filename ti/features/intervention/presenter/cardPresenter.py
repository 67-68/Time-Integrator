from PyQt6.QtCore import QObject
from ti.features.intervention.formatter import InterventionFormatter
from ti.features.intervention.model.model import InterventionEvent, InterventionRecipe
from ti.features.intervention.view.card import InterventionCard
from ti.UI.widgets.other.BasicLabel import BasicLabel

class InterventionPresenter(QObject):
    def __init__(
        self,
        ui: InterventionCard,
        IF: InterventionFormatter,
        recipe: InterventionRecipe
    ):
        """
        管理Intervention的类
        它作为Intervention卡片的数据来源
        卡片的每个行动都作为事件传入
        """
        self.ui = ui
        self.id = ui.id
        self.IF = IF
        self.recipe = recipe

    def process_user_action(
        self,
        event: InterventionEvent
    ):
        """
        从Event中找到这种情况应该怎么做
        然后执行
        """
        
        
