from ti.UI.presenters.formatter import FormatService
from ti.features.intervention.formatter import InterventionFormatter
from ti.features.intervention.model.repository import InterventionRepository
from ti.features.intervention.model.model import InterventionFactory_Pack, InterventionRecipe
from ti.features.intervention.view.card import InterventionCard


class InterventionCard_Factory:
    def __init__(
        self,
        repository: InterventionRepository,
        formatter: InterventionFormatter
    ):
        """_summary_
        这个类用来制造UI卡片
        首先它会获取全部的配方
        制造出来之后返回
        Args:
            repository (InterventionRepository): _description_
        """
        self.repository = repository
        self.cards = {}
        self.formatter = formatter
    
    def create_cards(self) -> dict:
        """_summary_
        根据当前的预设配方生成卡片
        
        Returns:
            dict: _description_
        """
        recipes = self.repository.get_all_recipes()
        
        for recipe in recipes:
            # 首先获取数据
            recipe: InterventionRecipe
            id = recipe.intervention_id
            state = recipe.initial_state # 获取第一个状态
            
            data = self.formatter.format(id,state)
            
            title = data["title"]
            choices = data["choice"]        
            
            ui = InterventionCard(title,choices,id)

            # 这里创建返回包
            self.cards[id] = InterventionFactory_Pack(ui,recipe)
            
        return self.cards

    def reset(self):
        """_summary_
        清除所有生成了的卡片
        """
        self.cards = {}
        