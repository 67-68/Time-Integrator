import copy
from dataclasses import dataclass
from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.intervention.service.formatter import INV_Formatter
from ti.features.intervention.model.model import INV_Special_States, INV_View_ID, INV_State_Btn, INV_State_Presentation, INVEvent, INV_View_Recipe, INVState
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.symbol_service import SymbolService


class INV_Card_Repository(IYamlRepository):
    def __init__(
        self,
        formatter: INV_Formatter,
        symbol_service: SymbolService,
        yaml_parser: YamlParser
        ):
        self.formatter = formatter
        self.symbol = symbol_service
        self.yaml_parser = yaml_parser
        # 在初始化时加载配方数据
        self._recipes_data = self._load_data()
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/features/intervention/model/data/view_recipes.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/features/intervention/model/data/rules.yaml"
    
    def save(self):
        return super().save()
    def load(self):
        return super().load()
    
    def delete(self, id):
        return super().delete(id)
    
    def _load_data(self): #问题在这里，获取配方的时候获取的配方不完整
        """
        从YAML文件加载配方数据
        连同规则文件一起加载
        """
        try:
            # 检查规则文件是否为空
            rules_data = self.yaml.get_data(self.rule_file_path)
            
            if rules_data is None or rules_data == {}:
                # 规则文件为空，直接加载原始数据
                recipes_data = self.yaml.get_data(self.filePath)
                recipes_data = recipes_data.get('view_recipes', {}) if recipes_data else {}
            else:
                # 规则文件不为空，使用parse_data方法解析
                recipes_data = self.yaml.parse_data(self.filePath, self.rule_file_path)
                recipes_data = recipes_data.get('view_recipes', {})
            
            # 填充符号
            filled_recipes = self.symbol.fill_symbols(recipes_data)
            return filled_recipes
            
        except Exception as e:
            print(f"Error loading recipes data: {e}")
            return {}
    
    def get_data(self):
        """
        初始化的时候被调用
        """
        return self._recipes_data
    
    def get_all(self):
        """
        这个函数会返回所有配方。
        """
        recipe_dataClass = []
        
        for recipe_id in self._recipes_data:
            recipe_dataClass.append(self.get_by_id(recipe_id))
        
        return recipe_dataClass
    def get_by_id(self, view_recipe_id: str) -> INV_View_Recipe:
        """_summary_

        Args:
            intervention_id (str): _description_

        Returns:
            recipe: INV_Recipe
        """
        
        # 第一层 
        recipe_dataClass: INV_View_Recipe
        view_recipe_id = view_recipe_id.upper()
        recipe = self._recipes_data[view_recipe_id]
        id = recipe["id"]
        recipe_states = recipe["state"]
        detector = recipe["detector"] # TODO: 找不到detector
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

create_intervention = INV_Universal_State(
    "create_intervention",
    {
        "transition":{
            INVEvent.INTERVENTION_CREATED.value: "intervene_user" #到时候，这个事件会由presenter自己激发                        
        },
        "presentation":{
            "title": "ask_challenge",
            "button":{}
        },
        "special_event": [INV_Special_States.ACCEPTED_CONTRACT.value]
    },
)