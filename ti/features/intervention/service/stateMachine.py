from ti.features.intervention.model.model import INV_View_Recipe, INVState


class INV_StateService:
    def __init__(self):
        """_summary_
        这个类负责和事件和状态转换相关的服务
        它目前唯一的职责就是告诉presenter下一个状态是什么
        """
        pass
    def process_event(
        self,
        event_id: str, #按理来说它应该不是一个事件enum
        current_state_key: str,
        recipe: INV_View_Recipe
    ) -> INVState:
        """
        根据配方
        回答一个事件的下一个状态是什么
        如果出错返回空
        """    
        # 1. 获取当前状态的完整对象
        current_state: INVState = recipe.state.get(current_state_key)
                
        if not current_state:
            print(f"错误：在配方中找不到当前状态 '{current_state_key}'")
            return

        # 2. 从当前状态的转换规则(transition)中，查找此事件应该去往哪个新状态
        next_state_key = current_state.transition.get(event_id)
        
        if not next_state_key:
            print(f"警告：在状态 '{current_state_key}' 中没有为事件 '{event_id}' 定义转换规则。")
            # 在这里你可以决定是保持不动，还是进入一个错误/结束状态
            return
            
        # 3. 获取下一个状态的完整对象
        next_state: INVState = recipe.state.get(next_state_key) 
        
        if not next_state:
            print(f"错误：在配方中找不到目标状态 '{next_state_key}'")
            return
        
        return next_state        

    
    
    