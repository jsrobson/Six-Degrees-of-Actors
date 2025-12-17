# == Standard Library imports ==
from dataclasses import dataclass, field

@dataclass
class Film:
    """
    Dataclass for Film object. Attributes:
        title (str): The film's title.
        year (int): Year of release.
        rating (float): IMDb rating of the film.
        film_id (str): Unique identifier for the film.
        cast (List[str]): List of actors in the film.
    """
    name: str
    year: int
    rating: float
    id: str
    cast: list[str] = field(default_factory=list)

