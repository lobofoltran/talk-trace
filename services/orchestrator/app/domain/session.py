from dataclasses import dataclass

@dataclass(frozen=True)
class Session:
    id: str
    status: str  # recording | finished
