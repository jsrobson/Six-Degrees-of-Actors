from dataclasses import dataclass, field
from math import inf

@dataclass
class Actor:
    name: str
    id: str
    films: list[str]
    costars: set[str] = field(default_factory=set)
    explored: bool = field(default=False)
    bacon_number: int = field(default=inf)

    def restore_default(self):
        self.explored = False