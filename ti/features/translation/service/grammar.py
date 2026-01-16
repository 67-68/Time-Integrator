from ti.features.translation.model.parsers import Parsers as p

parse_time = p.parse_regex(r"^\d{4}|\d{2}","time")
parse_action_type = p.parse_regex(r"^[wrs]","action_type")
parse_action = p.parse_regex(r"^\S+","action")
parse_space = p.parse_literal(" ")

action_unit_parser = p.sequence(
    [parse_time,
    parse_time,
    parse_action_type,
    parse_action]
)

class Grammar:
    def __init__(self):
        pass
    def parse_line_action_unit(self,line: str):
        """
        解析单行速记文本。
        """
        result = action_unit_parser(line.strip())
        
        if result.success:
            # 在这里，我们可以把解析出的原始列表，
            # 转换成一个更友好的字典（这就是AST -> Final Data的转换）
            start, end, type_char, action = result.value
            
            return {
                "status": "success",
                "data": {
                    "start": start,
                    "end": end,
                    "action_type": type_char,
                    "action": action,
                },
                "remaining": result.remaining_text
            }
        else:
            return {"status": "error", "message": "Invalid syntax"}