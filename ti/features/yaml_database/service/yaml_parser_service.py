import yaml
from ti.core.Interfaces.yaml_parser_interface import IYamlParser


class YamlParser(IYamlParser):
    @property
    def rules_file_path(self):
        """
        '元'规则文件的数据
        规定规则文件应该怎么写
        """
        pass
    # 干脆直接硬编码python
        
    
    def parse_data(
        self,
        data_file_path,
        rules_file_path
    ):
        """
        解析数据
        
        Returns:
            _type_: _description_
        """
        super().parse_data()
        
        data_file = self.get_data(data_file_path)
        rule_data = self.get_data(rules_file_path)
        
        
    
    def get_data(self,file_path):
        try:
            # 使用 'with open' 是最佳实践，它能确保文件在操作后被正确关闭
            with open(file_path, 'r', encoding='utf-8') as file:
                # 使用 yaml.safe_load() 来解析 YAML 文件
                # 这比 yaml.load() 更安全，因为它能防止执行任意代码
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"错误: 配置文件 '{file_path}' 未找到。")
        except yaml.YAMLError as e:
            print(f"错误: 解析 YAML 文件时出错: {e}")

    def parse_rule(self,rule_file):
        """
        这个函数负责创建所有的规则解析文件
        """
        
    def create_parse_value(self,)
        
        
    
"""
规则文件形似
domain:
  key:
    - {whatever_key}: {whatever_text}
  value:
    - {whatever_value}: {whatever_text}

在解析的时候
每一个whatever_key都会被解析成为wahtever_text.whatever_key
例如
domain:
  key:
    detector_recipe: detector

解析的时候:
detector.detector_recipe: {whatever_value}
"""
