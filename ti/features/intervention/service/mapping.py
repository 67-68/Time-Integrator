from ti.features.intervention.model.entity_Recipe_Repository import INV_Entity_Recipe_Repository
from ti.features.intervention.model.model import INV_Entity_Recipe


class InterventionMapping:
    def __init__(self,entity_rep: INV_Entity_Recipe_Repository):
        """
        这个类负责把洞察卡片和干涉实体配方对应起来
        找出这张洞察卡片会激活什么干涉实体配方
        """
        self.entity_recipies: list[INV_Entity_Recipe] = entity_rep.get_all_recipes()
        self.mapping = {}
        if not self.entity_recipies:
            print("NO INTERVENTION ENTITY RECIPE!")
            return None
        
        for recipe in self.entity_recipies:
            insight_id = self.entity_recipies[recipe].insight_card_category_id
            if insight_id not in self.mapping:
                self.mapping[insight_id] = []
            self.mapping[insight_id].append(self.entity_recipies[recipe])
    
    def find_mapping(self,insight_card_id) -> list[str]:
        """
        用来查找这个id是否需要创建，会返回一堆key

        Args:
            insight_card_id (_type_): _description_

        Returns:
            list[str]: _description_
        """
        entities = self.mapping.get(insight_card_id, None)
        print(f"对于卡片{insight_card_id},找到{entities}")
        return entities