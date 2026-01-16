from enum import Enum

from ti.features.insight.model.insight_card_recipe_repository import Insight_Card_Recipe_Repository


class YamlEditMode(Enum):
    EDIT_INSIGHT = "edit_insight"
    EDIT_INTERVENTION = "edit_intervention"

class TI_YamlDesigner:
    def __init__(
        self
    ):
        self.editing_mode = YamlEditMode.EDIT_INSIGHT
        self.insight_recipe_path = "ti/features/insight/model/data/insight_card_recipes.yaml"
        self.insight_narrative = "ti/features/insight/model/data/insight_narratives.yaml"
        
    
    def initialize(self):
        while True:
            print("=" * 50)
            print("[YAML_DESIGNER]: start main loop")
            print("=" *20)
            print("[YAML_DESIGNER]-init \{name\} for adding a new card ")
            print("=" *20)
            print("=" * 50)
            ipt = input("enter command")
            
            if ipt.startswith("-init "):
                name = ipt[len("-init "):]
                
                
                
                
                
            
            
    def ask_for_sure(self,text):
        pass
        
        
    def shutdown(self):
        pass

        
    def choose_mode(self):
        print("=" * 20)
        print["[YAML_DESIGNER]: Choose your mode"]
        while True:
            print("[YAML_DESIGNER]: 1 for insight, 2 for intervention")
            choice = input("give your answer")
            if choice == 1:
                print("[YAML_DESIGNER]: you have switch to edit_insight")
                break
            elif choice == 2:
                print("[YAML_DESIGNER]: you have switch to edit_intervention")
                break
        print("end_switch mode")
        print("=" * 20)
    
    def create_pattern(self):
        pass
    
    def edit_insight(self):
        pass
        
    
    
