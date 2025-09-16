from dataclasses import dataclass


@dataclass
class ParseResult:
    success: bool
    value: any = None
    remaining_text: str = ""

