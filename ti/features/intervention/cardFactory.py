from dataclasses import dataclass
from ti.UI.presenters.formatter import FormatService # 假设这个保留，但 formatter 不再需要
from ti.features.intervention.model.repository import INV_Repository
from ti.features.intervention.model.model import INVRecipe, INVState
from ti.features.intervention.view.card import InterventionCard


class InterventionCard_Factory:
    def __init__(
        self,
        repository: INV_Repository
    ):
        """
        这个类用来制造UI卡片。
        它现在只需要一个 repository，因为它得到的配方已经是“成品”了。
        """
        self.repository = repository
        self.cards = {}
        # self.formatter 依赖已被移除
    
    def create_cards(self) -> dict:
        """
        根据当前的预设配方生成卡片。
        这个方法现在变得非常简洁。
        """
        # 1. 从 repository 获取所有完整且格式化好的配方
        recipes = self.repository.get_all_recipes()
        
        for recipe in recipes:
            recipe: INVRecipe
            id = recipe.intervention_id
            
            # 2. 直接从配方对象中获取初始状态的展示数据
            # recipe 对象中的文本已经是被 Formatter 处理过的最终版本
            initial_state_key = recipe.initial_state
            initial_state: INVState = recipe.state[initial_state_key]
            
            presentation = initial_state.presentation
            
            # 3. 提取标题和按钮文本
            title = presentation.title
            
            # 将按钮对象字典转换为 {"event_id": "button_text"} 的简单字典
            # 这是UI组件（InterventionCard）更喜欢的数据格式
            choices = {
                btn_id: btn_obj.text 
                for btn_id, btn_obj in presentation.button.items()
            }
            
            # 4. 创建 UI 卡片实例
            ui = InterventionCard(title, choices, id)

            # 5. 创建并存储返回包
            self.cards[id] = InterventionFactory_Pack(ui, recipe)
            
        return self.cards

    def reset(self):
        """
        清除所有生成了的卡片。
        """
        self.cards = {}
        
        
@dataclass
class InterventionFactory_Pack:
    ui: InterventionCard
    recipe: INVRecipe
    