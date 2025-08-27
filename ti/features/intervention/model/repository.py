import copy
from ti.features.intervention.formatter import INV_Formatter
from ti.features.intervention.model.model import INV_ID, INV_State_Btn, INV_State_Presentation, INVEvent, INVRecipe, INVState


class INV_Repository:
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
        """
        重写后的方法，适配了新的 formatter.format()。
        现在它会为每个状态调用一次format方法，来获取所有格式化后的文本，
        而不是在按钮循环中为每个按钮单独调用。
        """
            
        recipe = copy.deepcopy(recipes[intervention_id])
        id = recipe["id"]
        recipe_states = recipe["state"]
        detector = recipe["detector"]
        initial_state = recipe["initial_state"]
        
        states_dataClass = {}
        
        for state_key in recipe_states:
            state = recipe_states[state_key]
            
            # --- 核心改动开始 ---
            formatted_texts = self.formatter.format(intervention_id, state_key)
            
            # 从格式化后的文本包中提取标题和按钮文本
            formatted_title = formatted_texts["title"]
            formatted_buttons_text = formatted_texts["buttons"]
            # --- 核心改动结束 ---

            # 创建Transitions
            transitions = state["transition"]
            
            # 创建Presentation
            presentation = state["presentation"]
            pre_copy = copy.deepcopy(presentation)
            buttons_structure = pre_copy["button"]
            
            button_dataClasses = {}
            
            for button_id in buttons_structure:
                # 2. 直接从 formatted_buttons_text 中获取对应按钮的文本
                # 不再需要判断 text_key 或 text
                text = formatted_buttons_text[button_id]
                eventReturn = button_id
                                    
                button_dataClasses[button_id] = INV_State_Btn(eventReturn, text)
            
            # 3. 使用格式化后的标题创建 Presentation DataClass
            pre_dataClass = INV_State_Presentation(button_dataClasses, formatted_title)
            
            # 创建并存储 State DataClass
            states_dataClass[state_key] = INVState(state_key, transitions, pre_dataClass)
        
        
        recipe_dataClass = INVRecipe(id, states_dataClass, initial_state, detector)
        
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
        "detector":None
    }
}