from dataclasses import dataclass, field

@dataclass
class Film:
    name: str
    year: int
    rating: float
    id: str
    cast: list[str] = field(default_factory=list)

