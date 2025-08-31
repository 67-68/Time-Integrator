from dataclasses import dataclass
from ti.UI.presenters.formatter import FormatService # 假设这个保留，但 formatter 不再需要
from ti.features.intervention.model.view_repository import INV_Card_Repository
from ti.features.intervention.model.model import INV_View_Recipe, INVState
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.view.interventionCard import InterventionCard


class INV_Card_Factory:
    def __init__(
        self,
        formatter: INV_Formatter
    ):
        """
        这个类用来制造UI卡片。
        它本身没有状态
        调用函数的时候传入依赖
        """
        self.format = formatter
    
    def create_card(
        self,
        recipe: INV_View_Recipe
    ) -> dict:
        """
        根据传入的配方生成卡片ui
        一次生成一张
        """
        intervention_id = recipe.intervention_id
        
        # 2. 直接从配方对象中获取初始状态的展示数据
        # recipe 对象中的文本已经是被 Formatter 处理过的最终版本
        initial_state_key = recipe.initial_state
        presentation = self.format.format(intervention_id,initial_state_key)
        
        # 3. 提取标题和按钮文本
        title = presentation["title"]
        choices = presentation["buttons"]
        
        # 4. 创建 UI 卡片实例
        ui = InterventionCard(title, choices, intervention_id)

        return ui
        

    def reset(self):
        """
        清除所有生成了的卡片。
        """
        self.cards = {}
        
        
@dataclass
class InterventionFactory_Pack:
    ui: InterventionCard
    recipe: INV_View_Recipe
    