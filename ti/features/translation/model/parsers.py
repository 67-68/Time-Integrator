import re
from ti.features.translation.model.parse_result import ParseResult


Parser = callable((str,ParseResult))

class Parsers:
    @staticmethod
    def parse_literal(preset_text) -> Parser:
        """
        解析字符串

        Args:
            str (_type_): _description_

        Returns:
            Parser: _description_
        """
        def parser(text: str) -> ParseResult:
            if text.startswith(preset_text):
                return ParseResult(
                    success = True,
                    value = preset_text,
                    remaining_text = text[len(preset_text):]
                )
            return ParseResult(success=False, remaining_text=text)
        return parser

    @staticmethod
    def parse_regex(pattern: str, name: str = "regex") -> Parser:
        """
        一个更强大的原子解析器，使用正则表达式。
        """
        compiled_pattern = re.compile(pattern)
        def parser(text: str) -> ParseResult:
            match = compiled_pattern.match(text)
            if match:
                value = match.group(0)
                return ParseResult(
                    success=True,
                    value=value,
                    remaining_text=text[len(value):]
                )
            return ParseResult(success=False, remaining_text=text)
        return parser
    
    @staticmethod
    def sequence(parsers: list[Parser]) -> Parser:
        """
        【组合子】：将一系列解析器串联起来。
        必须按顺序全部成功。
        """
        def parser(text: str) -> ParseResult:
            results = []
            current_text = text
            for p in parsers:
                result = p(current_text)
                if not result.success:
                    return ParseResult(success=False, remaining_text=text) # 注意：回溯到原始文本
                results.append(result.value)
                current_text = result.remaining_text
            return ParseResult(success=True, value=results, remaining_text=current_text)
        return parser   
    
    @staticmethod
    def many(parser_to_repeat: Parser) -> Parser:
        """

        【组合子】：重复一个解析器0次或多次。
        """
        def parser(text: str) -> ParseResult:
            results = []
            current_text = text
            while True:
                result = parser_to_repeat(current_text)
                if not result.success:
                    break
                results.append(result.value)
                current_text = result.remaining_text
            
            # many总是“成功”的，即使它什么也没匹配到（返回一个空列表）
            return ParseResult(success=True, value=results, remaining_text=current_text)
        return parser
    
    @staticmethod
    def parse_literals(literals):
        def parser(text: str):
            for literal in literals:
                result:ParseResult = Parsers.parse_literal(literal)
                if result.success == True:
                    return result
                
            return result
        return parser