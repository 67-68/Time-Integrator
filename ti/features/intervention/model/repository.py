import copy
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.model.model import INV_ID, INV_State_Btn, INV_State_Presentation, INVEvent, INV_View_Recipe, INVState


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
    
    def get_recipe_by_id(self, intervention_id: str):
        """_summary_

        Args:
            intervention_id (str): _description_

        Returns:
            recipe: INV_Recipe
        """
        
        # 第一层 
        recipe_dataClass: INV_View_Recipe
        recipe = recipes[intervention_id]
        id = recipe["id"]
        recipe_states = recipe["state"]
        detector = recipe["detector"]
        initial_state = recipe["initial_state"]
        
        
        # 第二层: States
        states_dataClass = {}
        
        for state_key in recipe_states:
            state = recipe_states[state_key]
            transitions = state["transition"]
            presentation = state["presentation"]
            
            # 第三层: Presentation
            button_dataClasses = {}
            
            button_recipes = presentation["button"]
            title = presentation["title"]
            
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
            
            states_dataClass[state_key] = INVState(
                state_key,
                transitions,
                pre_dataClass
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

recipes = {
    INV_ID.POST_EAT_WASTE.value: {
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
                }
            },
            "create_intervention":{
                "transition":{
                    INVEvent.INTERVENTION_CREATED.value: "intervene_user" #到时候，这个事件会由presenter自己激发                        
                },
                "presentation":{
                    "title": "接收挑战！",
                    "button":{}
                }
            }
        },
        "initial_state":"init",
        "detector":None #应该是在后面获取了卡片的Detector
    }
}


# TODO: 修改卡片的Detector配方为数据模型，同时加上hook和result的matcher作为分别