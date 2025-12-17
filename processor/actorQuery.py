# == Standard Library imports ==
from collections import deque
from dataclasses import dataclass
from math import inf
from typing import Dict, List

# == Local import
from models import Actor

@dataclass
class PathSegment:
    """
    Represents a segment of the actor path, storing two actors and the films
    shared between them.
    """
    actor1: str
    actor2: str
    shared_films: List[str]

def generate_actors_path(start: str, end: str, prev: Dict[str, str]) \
        -> List[str]:
    """
    Generate a path from the starting actor to end actor using 'prev' mapping.

    :param start: Starting actor name.
    :param end: Ending actor name.
    :param prev: Dictionary mapping actor name to previous actor in path.
    :return: List of actor names from start to end, empty if no path exists.
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = prev.get(current)
    else:
        return []
    path.reverse()
    return path

def generate_complete_path(actors_dict: Dict[str, Actor], path: List[str]) \
        -> dict[int, PathSegment]:
    """
    Given a list of actors, build a mapping of actor pairs to their shared
    films.

    :param actors_dict: Dictionary mapping actor name to Actor object.
    :param path: List of actor names representing the path from origin to
    destination.
    :return: Dictionary mapping pair index to PathSegment objects.
    """
    return {
        i: PathSegment(
            actor1=curr_actor,
            actor2=next_actor,
            shared_films=sorted(
                set(actors_dict[curr_actor].films) & set(actors_dict[next_actor].films)
            )
        )
        for i, (curr_actor, next_actor) in enumerate(zip(path, path[1:]))
    }
class ActorQuery:
    """
    Represents a query to compute the Bacon number and shortest path between
    two given actors.

    Attributes:
        act_origin (str): Name of the origin actor.
        act_destination (str): Name of the destination actor.
        valid_origin (bool): Whether the origin actor exists in the dataset.
        valid_destination (bool): Whether the destination actor exists in
        the dataset.
        bacon_number (float): The computed Bacon number (distance) from
        origin to destination.
        complete_path (Dict[int, PathSegment]): Mapping of actor pair index
            to ((actor1, actor2), list of shared films along the path.

    """
    def __init__(self, actor_1: str, actor_2: str):
        """
        Initialize an ActorQuery with two actor names.
        :param actor_1: Name of the starting actor.
        :param actor_2: Name of the destination actor.
        """
        self.act_origin: str = actor_1
        self.act_destination: str = actor_2
        self.valid_origin: bool = False
        self.valid_destination: bool = False
        self.bacon_number: float = inf
        self.complete_path: Dict[int, PathSegment] = {}

    def _check_valid(self, actors_dict: dict[str, Actor]) -> (bool, List[str]):
        """
        Check if origin and destination actors exist in the actors dictionary.

        :param actors_dict: Mapping from actor names to Actor objects.
        :return: Tuple of (is_valid, messages).
        """
        messages: List[str] = []
        self.valid_origin = self.act_origin in actors_dict.keys()
        self.valid_destination = self.act_destination in actors_dict.keys()

        if not self.valid_origin:
            messages.append(f"First actor {self.act_origin} not found.")
        if not self.valid_destination:
            messages.append(f"Second actor {self.act_destination} not found.")

        return self.valid_origin and self.valid_destination, messages

    # assume dictionary containing k: actor name, v: actor objects
    def run_bfs(self, actors_dict: dict) -> None:
        """
        Compute the shortest path (Bacon number) from origin to destination
        using breadth-first search (BFS). Updates self.bacon_number and
        self.complete_path.

        :param actors_dict: Dictionary mapping actor names to Actor objects.
        """
        # check is valid (both actors present)
        is_valid, messages = self._check_valid(actors_dict)
        if not is_valid:
            for msg in messages: print(msg)
            return

        # check not self
        if self.act_origin == self.act_destination:
            print("Origin is same as destination")
            self.bacon_number = 0
            self.complete_path = {}
            return

        # initialize BFS
        for actor in actors_dict.values():
            actor.explored = False
            actor.bacon_number = inf

        # mark origin as explored, all other vertices as unexplored
        actors_dict[self.act_origin].explored = True
        # distance from self is 0
        actors_dict[self.act_origin].bacon_number = 0

        # initialize queue data structure, with origin as initial entry
        queue = deque([actors_dict[self.act_origin]])
        # dict to store previous path nodes
        prev: Dict[str, str] = {}

        while queue:
            # get the current actor and current distance
            current_actor = queue.popleft()
            current_distance = current_actor.bacon_number
            for costar in current_actor.costars:
                neighbour = actors_dict[costar]
                if not neighbour.explored:
                    # mark costar as explored
                    neighbour.explored = True
                    #l(costar) = l(actor) + 1
                    neighbour.bacon_number = current_distance + 1
                    # add costar to end of queue
                    queue.append(neighbour)
                    # store prev path
                    prev[neighbour.name] = current_actor.name
        # update paired bacon number
        self.bacon_number = actors_dict[self.act_destination].bacon_number
        # generate simple actors path and use it to build a complete path
        path = generate_actors_path(self.act_origin, self.act_destination, prev)
        self.complete_path = generate_complete_path(actors_dict, path)

    def _get_path_strings(self) -> List[str]:
        """
        Return a list of formatted strings represented the Bacon number path.

        Each string describes the Bacon number and shared film for each
        actor pair along the path. Does not print to console, making it
        testable.

        :return: List of strings representing the path and shared films.
        """
        # failsafe if no path present
        if self.bacon_number == float('inf'):
            return [f"No path found from {self.act_origin} to "
                    f"{self.act_destination}."]

        # initialize bacon number string
        output: List[str] = [
            f"{self.act_destination} has a Bacon number of {self.bacon_number} "
            f"from {self.act_origin}."
        ]
        # for each segment in path, get shared filmography
        for index, segment in sorted(self.complete_path.items()):
            films_str = ", ".join(segment.shared_films)
            output.append(f"{index + 1}: {segment.actor1} and "
                          f"{segment.actor2} starred together in {films_str}")
        return output

    def print_string(self) -> None:
        """
        Print the Bacon number and the detailed actor path to the console.

        This method retrieves the formatted path strings (using supporting
        _get_path_strings method) and prints them one by one. Each line
        shows either the Bacon number for origin to destination or a pair of
        actors and the films they shared.
        """

        print("\nBACON NUMBER")
        for item in self._get_path_strings():
            print(item)