import yaml
from ti.core.Interfaces.yaml_parser_interface import IYamlParser
from ti.features.yaml_database.model.rules import LineRuleItem, RuleFile, TextRuleItem, RuleBlock


class YamlParser(IYamlParser):
    @property
    def rules_file_path(self):
        """
        '元'规则文件的数据
        规定规则文件应该怎么写
        """
        pass
    # 干脆直接硬编码python
    
    def load_rules(self, rules_file_path: str) -> RuleFile:
        """
        用来解析yaml文件自带的rules文件

        Args:
            rules_file_path (str): _description_
        """
        if not rules_file_path:
            print(f"[YAML_PARSER]: No data in rule file {rules_file_path}")
        
        rule_file = self.get_data(rules_file_path)
        
        # 如果rule_file为空，创建空的RuleFile对象
        if rule_file is None:
            print(f"[YAML_PARSER]: Rule file {rules_file_path} is empty, creating empty RuleFile")
            empty_domain = RuleBlock(key_rules=[], value_rules=[], line_rules=[])
            return RuleFile(domain=empty_domain)
        
        try:
            # --- 核心步骤 ---
            # 使用 RuleFile.model_validate() 将字典转换为类型安全的 Pydantic 对象
            # 如果 rule_dict 的结构或类型不符合 RuleFile 的定义，这里会抛出详细的 ValidationError
            validated_rules = RuleFile.model_validate(rule_file)
            print("规则文件解析和验证成功！")
            return validated_rules
        except Exception as e:
            # Pydantic 的 ValidationError 提供了非常清晰的错误信息
            print(f"错误: 规则文件 '{rules_file_path}' 格式不正确。")
            print(f"详细信息: {e}")
            # 返回空的RuleFile对象而不是None
            empty_domain = RuleBlock(key_rules=[], value_rules=[], line_rules=[])
            return RuleFile(domain=empty_domain)
    def create_key_parser(self,rules: TextRuleItem):
        def key_parser(key):
            return key
        return key_parser
        
    def create_value_parser(self,rules: TextRuleItem):
        def value_parser(value):
            return value
        return value_parser
        
    def create_line_parser(
        self,
        rules: list[LineRuleItem],
        value_parser,
        key_parser
    ):
        prefix_value = {}
        
        for rule in rules:
            if rule.add_prefix:
                    prefix = rule.add_prefix.prefix
                    value = rule.add_prefix.key
                    prefix_value[value] = prefix
                    
            def line_parser(line:dict):
                prefixs = prefix_value
                
                for key in line:
                    value = line[key]
                    key = key_parser(key)
                    value = value_parser(value)
                    
                    if key in prefixs:
                        newline = {
                            key: prefix + line[key]
                        }
                        return newline
                            
            return line_parser
            

    
    def create_file_parser(self,rules:RuleFile):
        # Create key parser
        key_parser = self.create_key_parser(rules.domain.key_rules[0] if rules.domain.key_rules else None)
        
        # Create value parser
        value_parser = self.create_value_parser(rules.domain.value_rules[0] if rules.domain.value_rules else None)
        
        # Create line parser
        line_parser = self.create_line_parser(
            rules.domain.line_rules,
            value_parser,
            key_parser
        )
        
        def file_parser(data):
            result = {}
            if isinstance(data, dict):
                for key, value in data.items():
                    parsed_line = line_parser({key: value})
                    result.update(parsed_line)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        parsed_line = line_parser(item)
                        result.update(parsed_line)
            return result
        
        return file_parser
    

    def parse_data(
        self,
        data_file_path,
        rules_file_path
    ):
        """
        解析数据
        
        Returns:
            dict: 解析后的数据字典
        """
        super().parse_data()
        
        # 加载数据文件和规则文件
        data = self.get_data(data_file_path)
        rules = self.load_rules(rules_file_path)
        
        if data is None:
            print(f"错误: 无法加载数据文件 '{data_file_path}'")
            return {}
            
        # 现在load_rules总是返回RuleFile对象，不会返回None
        # 即使规则文件无效或为空，也会返回空的RuleFile对象
        
        # 创建文件解析器并解析数据
        file_parser = self.create_file_parser(rules)
        parsed_data = file_parser(data)
        
        return parsed_data
    
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
