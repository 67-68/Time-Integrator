import copy
from dataclasses import dataclass
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.model.model import INV_Special_States, INV_View_ID, INV_State_Btn, INV_State_Presentation, INVEvent, INV_View_Recipe, INVState


class INV_Card_Repository:
    def __init__(
        self,
        formatter: INV_Formatter
        ):
        self.formatter = formatter
    
    def get_all_recipes(self):
        """
        这个函数会返回所有配方。
        """
        recipe_dataClass = []
        
        for recipe_id in recipes:
            recipe_dataClass.append(self.get_recipe_by_id(recipe_id))
        
    
        return recipe_dataClass
    def get_recipe_by_id(self, view_recipe_id: str) -> INV_View_Recipe:
        """_summary_

        Args:
            intervention_id (str): _description_

        Returns:
            recipe: INV_Recipe
        """
        
        # 第一层 
        recipe_dataClass: INV_View_Recipe
        recipe = recipes[view_recipe_id]
        id = recipe["id"]
        recipe_states = recipe["state"]
        detector = recipe["detector"]
        initial_state = recipe["initial_state"]
        
        
        # 第二层: States
        states_dataClass = {}
        
        for state_key in recipe_states:
            state = recipe_states[state_key]
            transitions = state.get("transition",None)
            presentation = state.get("presentation",None)
            special_event = state.get("special_event",None)
            
            # 第三层: Presentation
            if presentation:
                button_dataClasses = {}
                
                button_recipes = presentation.get("button",None)
                title = presentation.get("title")
                
                # 第四层: Button
                for button_id in button_recipes:
                    text_key = button_recipes[button_id] #全部使用text_key
                    returnEvent = button_id
                    button_dataClasses[button_id] = INV_State_Btn(
                        returnEvent, 
                        text_key
                    )
                # 第四层结束
                
                pre_dataClass = INV_State_Presentation(
                    button_dataClasses,
                    title
                )
                # 第三层结束
            else:
                pre_dataClass = None
            
            states_dataClass[state_key] = INVState(
                state_key,
                transitions,
                pre_dataClass,
                special_event
            )
            # 第二层结束
        
        recipe_dataClass = INV_View_Recipe(
            id,
            states_dataClass,
            initial_state,
            detector
        )
        # 第一层结束
        
        
        return recipe_dataClass

# --- 以下为您提供的上下文代码，保持不变 ---
@dataclass
class INV_Universal_State:
    name: str
    value: dict
    
end_intervention = INV_Universal_State(
    "end_intervention",
    {"special_event": [INV_Special_States.END_INTERVENTION.value]} # 那么，应该首先检测这个。因此transition和presentation就不用写了
)

recipes = {
    INV_View_ID.POST_EAT_WASTE.value: {
        "id":"post_eat_waste",
        "state":{
            "init": {
                "transition":{
                    INVEvent.USER_ACCEPTED.value:"create_intervention", 
                    INVEvent.USER_REJECTED.value:"ask_attribution"
                },
                "presentation": {
                    "button": {
                        # 这个结构现在只定义了逻辑上的按钮存在性，
                        # 文本完全由 Formatter 和 Narrations 决定
                        INVEvent.USER_ACCEPTED.value: {
                            "text_key": "accept_challenge" 
                        },
                        INVEvent.USER_REJECTED.value: {
                             "text_key": "reject_challenge"
                        }
                    },
                    "title": "ask_challenge" # 这个key现在也只是一个逻辑标识
                },
            },
            "create_intervention":{
                "transition":{
                    INVEvent.INTERVENTION_CREATED.value: "intervene_user" #到时候，这个事件会由presenter自己激发                        
                },
                "presentation":{
                    "title": "ask_challenge",
                    "button":{}
                },
                "special_event": [INV_Special_States.ACCEPTED_CONTRACT.value]
            },
            "intervene_user":{
                "transition":{
                    INVEvent.USER_ACCEPTED.value: "end_intervention",
                    INVEvent.USER_REJECTED.value: "end_intervention" # 定义特殊状态? 或者复用Universal状态？
                },
                "presentation":{
                    "title":"你是不是要干坏事了?",
                    "button":{
                        INVEvent.USER_ACCEPTED.value: {
                            "text_key": "accept_challenge"
                        },
                        INVEvent.USER_REJECTED.value: {
                             "text_key": "reject_challenge"
                        }
                    }
                }
            },
            end_intervention.name: end_intervention.value
        },
        "initial_state":"init",
        "detector":None #应该是在后面获取了卡片的Detector
    }
}


# TODO: 修改卡片的Detector配方为数据模型，同时加上hook和result的matcher作为分别