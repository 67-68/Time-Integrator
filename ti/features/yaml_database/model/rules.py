from pydantic import BaseModel, Field

class TextReplaceRule(BaseModel):
    """
    基本的替换文本规则，作用于text value/key

    Args:
        BaseModel (_type_): _description_
    """
    target: str
    result: str
    description: str = ""
    
class TextRuleItem(BaseModel):
    """
    简单的ruleItem, 用来替换文本
    作用于key/value

    Args:
        BaseModel (_type_): _description_
    """
    text_replace: TextReplaceRule = None

class add_prefix_to_val_by_key(BaseModel):
    prefix: str
    key: str
    description:str = ""

class LineRuleItem(BaseModel):
    add_prefix: add_prefix_to_val_by_key = None
    
class RuleBlock(BaseModel):
    """
    表示总体所有的规则集合

    Args:
        BaseModel (_type_): _description_
    """
    key_rules: list[TextRuleItem] = Field(alias='key', default_factory=list)
    value_rules: list[TextRuleItem] = Field(alias='value', default_factory=list)
    line_rules: list[LineRuleItem] = Field(alias='line', default_factory=list)

class RuleFile(BaseModel):
    """
    一个文件

    Args:
        BaseModel (_type_): _description_
    """
    domain: RuleBlock
    
    


"""
basic modules:
- line
- key
- value
- block(start from "a" line, and have indicators to show the start and end of block) too complex to do it

these modules(key,val) can be added type rules?
- list
- dict?

whatever, the rule of replace can be used to key and val
the rule form should be
{
    key:
        text_replace:
            abc
            abg
            replace c -> g
    val
    line
}
"""