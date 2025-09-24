"""
特殊的，有固定效果的事件
"""
from dataclasses import dataclass
from typing import Literal

from ti.core.Interfaces.basic_event import BasicEvent


@dataclass
class ContractAgreementSubmitted(BasicEvent):
    contract_id: str
    choice: Literal["accepted", "declined"]
    
    