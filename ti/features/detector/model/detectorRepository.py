from enum import Enum
from ti.features.detector.model import userMatchers
from ti.features.detector.service.matchers import Matcher
from ti.features.detector.model.baseDetector import BaseDetector
from ti.features.detector.model.model import Detector_Config, Detector_Recipe, Detector_Recipe_ID, Detector_Sequence, Detector_State
from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.yaml_database.service.yaml_parser_service import YamlParser


class DetectorRepository(IYamlRepository):
    def __init__(self, yaml_parser: YamlParser = None):
        """_summary_
        这个类负责存储字典形式的配方并通过数据模型类把他们组装起来
        """
        self.yaml_parser = yaml_parser or YamlParser()
        self.recipes_data = self._load_data()
    
    @property
    def yaml(self):
        return self.yaml_parser
    
    @property
    def filePath(self):
        return "ti/model/data/detector_recipes.yaml"
    
    @property
    def rule_file_path(self):
        return "ti/model/data/detector_recipes_rules.yaml"
    
    def _load_data(self):
        """
        从YAML文件加载配方数据
        """
        try:
            # 检查规则文件是否为空
            rules_data = self.yaml.get_data(self.rule_file_path)
            
            if rules_data is None or rules_data == {}:
                # 规则文件为空，直接加载原始数据
                recipes_data = self.yaml.get_data(self.filePath)
                recipes_data = recipes_data.get('detector_recipes', {}) if recipes_data else {}
            else:
                # 规则文件不为空，使用parse_data方法解析
                recipes_data = self.yaml.parse_data(self.filePath, self.rule_file_path)
                recipes_data = recipes_data.get('detector_recipes', {})
            
            return recipes_data
            
        except Exception as e:
            print(f"Error loading detector recipes data: {e}")
            return {}
    
    def save(self):
        """
        保存数据到YAML文件
        """
        try:
            data_to_save = {
                'detector_recipes': self.recipes_data
            }
            from ti.services.dataAccess import save_yaml_data
            save_yaml_data(data_to_save, self.filePath)
            return True
        except Exception as e:
            print(f"Error saving detector recipes data: {e}")
            return False
    
    def load(self):
        """
        从YAML文件加载数据
        """
        self.recipes_data = self._load_data()
        return self.recipes_data
    
    def get_by_id(self, id: str):
        """
        通过id获取配方数据
        """
        return self.recipes_data.get(id, {})
    
    def get_all(self):
        """
        获取所有配方数据
        """
        return self.recipes_data
    
    def delete(self, id: str):
        """
        删除指定id的配方数据
        """
        if id in self.recipes_data:
            del self.recipes_data[id]
            self.save()
            return True
        return False
    
    def get_recipe_by_id(self,detector_id:Detector_Recipe_ID) -> Detector_Recipe:
        """_summary_
        这个类接受一个Detector id
        根据id寻找配方组合为配方数据模型
        返回
        Args:
            id (Detector_Recipe_ID): _description_

        Returns:
            Detector_Recipe: _description_
        """
        if isinstance(detector_id,Detector_Recipe_ID):
            recipe_id = detector_id.value
        else:
            recipe_id = detector_id
            
        recipe = self.recipes_data.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe not found for id: {recipe_id}")
            
        sequences = recipe["config"]["sequence"]
    
        # HOOK部分
        hook_recipe = sequences["hook"]
        hook_dataClass = []
        result_recipe = sequences["result"]
        result_dataClass = []
        
        # 解析matcher字符串为实际的matcher函数
        matcher_instance = Matcher()
        
        # 创建状态数据模型
        for state in hook_recipe:
            state_name = state["state_name"]
            matcher_str = state["matcher"]
            matcher_func = self._parse_matcher_string(matcher_str, matcher_instance)
            hook_dataClass.append(Detector_State(state_name, matcher_func))
            
        for state in result_recipe:
            state_name = state["state_name"]
            matcher_str = state["matcher"]
            matcher_func = self._parse_matcher_string(matcher_str, matcher_instance)
            result_dataClass.append(Detector_State(state_name, matcher_func))
        
        sequence_dataClass = Detector_Sequence(
            hook_dataClass,
            result_dataClass
        )
        
        # 创建Config数据模型
        config_dataClass = Detector_Config(sequence_dataClass) 
        
        # 创建Recipe数据模型
        detector_type_str = recipe["detector"]
        # 将字符串转换为类引用
        if detector_type_str == "BaseDetector":
            detector_type = BaseDetector
        else:
            # 可以扩展支持其他detector类型
            detector_type = BaseDetector
        recipe_dataClass = Detector_Recipe(detector_type,config_dataClass)

        return recipe_dataClass
    
    def _parse_matcher_string(self, matcher_str: str, matcher_instance: Matcher):
        """
        解析matcher字符串为实际的matcher函数
        例如: "action_is('吃饭')" -> matcher_instance.action_is('吃饭')
        """
        try:
            # 检查是否是预定义的复杂matcher
            if matcher_str == "more_than_10_minute_waste":
                return matcher_instance.matchAll(
                    matcher_instance.action_type_is("waste"),
                    matcher_instance.duration_is_greater_than(10)
                )
            
            # 解析函数调用格式: function_name("arg")
            if "(" in matcher_str and ")" in matcher_str:
                func_name = matcher_str.split("(")[0]
                args_str = matcher_str.split("(")[1].rstrip(")")
                
                # 解析参数
                if args_str.startswith("'") and args_str.endswith("'"):
                    # 字符串参数
                    arg = args_str.strip("'")
                elif args_str.isdigit():
                    # 数字参数
                    arg = int(args_str)
                else:
                    # 其他情况，直接使用字符串
                    arg = args_str
                
                # 获取matcher方法并调用
                if hasattr(matcher_instance, func_name):
                    matcher_func = getattr(matcher_instance, func_name)
                    return matcher_func(arg)
            
            # 如果无法解析，返回一个总是返回False的matcher
            def default_matcher(au):
                return False
            return default_matcher
            
        except Exception as e:
            print(f"Error parsing matcher string '{matcher_str}': {e}")
            # 返回一个总是返回False的matcher作为fallback
            def fallback_matcher(au):
                return False
            return fallback_matcher

matcher = Matcher()


more_than_10_minute_waste = matcher.matchAll(
    matcher.action_type_is("waste"),
    matcher.duration_is_greater_than(10)
)





RECIPE = {
    Detector_Recipe_ID.POST_EAT_WASTE.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "meal",
                        "matcher": matcher.action_is("吃饭")
                    },
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": matcher.action_type_is("waste")
                    }
                ]
            }
        }
    },
    Detector_Recipe_ID.UNSETTLING_HEART.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "trivious_thing_1",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                    {
                        "state_name": "trivious_thing_2",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                    {
                        "state_name": "trivious_thing_3",
                        "matcher": matcher.duration_is_smaller_than(11)
                    },
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": more_than_10_minute_waste
                    }
                ]
            }
        }
    },
    Detector_Recipe_ID.POST_BASH_WASTE.value: {
        "detector": BaseDetector,
        "config":{
            "sequence": {
                "hook": [
                    {
                        "state_name": "bash",
                        "matcher": matcher.action_is("洗澡")
                    }
                ],
                "result":[
                    {
                        "state_name": "waste",
                        "matcher": matcher.action_type_is("waste")
                    }
                ]
            }
        }
    },
}


