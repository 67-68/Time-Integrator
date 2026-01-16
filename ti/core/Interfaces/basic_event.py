from dataclasses import dataclass
from typing import Protocol


@dataclass
class BasicEvent(Protocol):
    event_id: str