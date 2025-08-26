from ti.features.intervention.model.model import InterventionState
from ti.features.intervention.model.narratives import InterventionNarrator
from ti.utils import randomChoser


class InterventionFormatter:
    def __init__(
        self,
        IN: InterventionNarrator
    ):
        self.IN = IN
    
    def format(
        self,
        intervention_id: str,
        state: InterventionState
        ) -> dict:
        """_summary_
        这个函数用来提供文本,
        从Narrative中获取
        情景: 被Factory调用，塞进一个id来获取数据
        
        它首先会从Narrative获取数据
        然后替换
        Args:
            id (str): _description_
            state (InterventionState): _description_

        Returns:
            dict: {
                "title": intervention_title,
                "choice": choice,
                "id": id,
                "state":state
            }
        """
        # 首先获取对应ID数据
        sementic_id = state
        data = self.IN.get_text_by_id(intervention_id,sementic_id)

        intervention_title_list = data["presentation"]["title"]
        intervention_title = randomChoser(intervention_title_list)
        
        choice = {}
        
        intervention_choices_data = data["choice"]
        for choice_id in intervention_choices_data:
            choice_text = randomChoser(intervention_choices_data[choice_id])
            choice[choice_id] = choice_text
        
        pack = {
            "title": intervention_title,
            "choice": choice,
            "id": id,
            "state":state
        }
        
        return pack
        