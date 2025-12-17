# == Standard Library imports ==
from math import inf

# == Local imports ==
from dataclasses import dataclass, field

@dataclass
class Actor:
    """
    Represents an actor in the film network.

    Each Actor object contains identifying information, filmography,
    co-star relationships, and state attributes used for graph traversal.

    Attributes:
        name (str): Actor's full name.
        id (str): Unique identifier for the actor.
        films (List[str]): List of films the actor has appeared in.
        costars (Set[str]): Set of actor names who have co-starred with this actor.
        explored (bool): Whether the actor has been visited in a graph search.
        bacon_number (int): Distance from a starting actor in a graph traversal
            (e.g., Bacon or Erdős number). Defaults to infinity.
    """
    name: str
    id: str
    films: list[str]
    costars: set[str] = field(default_factory=set)
    explored: bool = field(default=False)
    bacon_number: int = field(default=inf)

    def restore_default(self) -> None:
        """
        Reset the actor's explored state to its default value. Useful for
        re-running graph traversals without recreating Actor objects.
        """
        self.explored = False