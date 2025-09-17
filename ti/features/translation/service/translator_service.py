from ti.features.translation.service.grammar import Grammar
from ti.services.translation.propertyTranslation import transPropToFast_API


class Translator:
    def __init__(
        self,
    ):
        self.grammar = Grammar()
        
    
    def translate(self,text):
        return self.grammar.parse_line_action_unit(text)
    
    def translate_property_to_fast_entry(self, property_data):
        """
        将属性数据翻译为快速输入文本
        :param property_data: 属性字典
        :return: 快速输入文本
        """
        # 转换属性字典格式以匹配transPropToFast_API的期望格式
        converted_properties = {
            "start": property_data.get('start'),
            "end": property_data.get('end'),
            "action_type": property_data.get('action_type'),
            "action": property_data.get('action'),
            "action_detail": property_data.get('action_detail')
        }
        return transPropToFast_API(converted_properties)
    
    def translate_fast_entry_to_property(self, fast_entry_text):
        """
        将快速输入文本翻译为属性数据
        :param fast_entry_text: 快速输入文本
        :return: 属性字典
        """
        # 使用现有的语法解析器
        action_unit = self.grammar.parse_line_action_unit(fast_entry_text)
        data = action_unit.get("data",None)
        if data:
            # 格式化时间 - 将1112转换为11:12
            start_time = self._format_time(data.get('start', ''))
            end_time = self._format_time(data.get('end', ''))
            
            # 如果end只有两位，取start的前两位填补
            if end_time and len(end_time) == 2 and start_time and len(start_time) >= 2:
                end_time = start_time[:2] + end_time
                end_time = self._format_time(end_time)  # 重新格式化
            
            action_type = data.get("action_type")
            if action_type == "w":
                action_type = "work"
            elif action_type == "s":
                action_type = "waste"
            elif action_type == "r":
                action_type = "rest"
            
            dict = {
                'start': start_time,
                'end': end_time,
                'action_type': action_type,
                'action': data.get('action', ''),
            }
            return dict
        return {}
    
    def _format_time(self, time_str):
        """
        格式化时间字符串，将1112转换为11:12
        :param time_str: 时间字符串
        :return: 格式化后的时间字符串
        """
        if not time_str:
            return ''
        
        # 移除所有非数字字符
        clean_time = ''.join(filter(str.isdigit, time_str))
        
        if len(clean_time) == 4:
            # 1112 -> 11:12
            return f"{clean_time[:2]}:{clean_time[2:4]}"
        elif len(clean_time) == 3:
            # 112 -> 01:12
            return f"0{clean_time[0]}:{clean_time[1:3]}"
        elif len(clean_time) == 2:
            # 12 -> 00:12 (保持原样，让上层处理)
            return clean_time
        elif len(clean_time) == 1:
            # 1 -> 00:01
            return f"00:0{clean_time}"
        else:
            # 其他情况返回原样
            return time_str