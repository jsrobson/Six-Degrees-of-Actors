# == Standard Library import
from pathlib import Path
# == Third party import
import pandas as pd
# == Local import
from models import Actor

INPUT_MSG = "USER INPUT"

def _get_user_input() -> tuple[str, str]:
    """
    Prompt the user for two actor names via the command line.
    :return: Tuple containing the first and second actor names, in order.
    """
    print(INPUT_MSG)
    actor_1 = input("Please type the name of the first actor: ")
    actor_2 = input("Please type the name of the second actor: ")
    return actor_1, actor_2

def _process_actor_row(row: pd.Series, a_dict: dict) -> None:
    """
    Builds an actor object from fields in row of data.

    :param row: Pandas row information for actors, movies
    :param a_dict: Dictionary of actors (k: name, v: object)
    :return: nothing, dictionary updated.
    """
    # pull actor name, id, films from row
    act_name, act_id, films = row['Actor'], row['ActorID'], row['Film']
    # build actor object from data and set to actor name as key
    a_dict[act_name] = Actor(act_name, act_id, films)

def _build_cast_dict(df: pd.DataFrame) -> dict[str, list[str]]:
    """
    Build a mapping from film title to cast list. Groups input df by film
    and returns a dict where each key is film title and each value is list
    of actor names in the film.

    :param df: Movie data with Film and Actor columns.
    :return: Dict, key (film title) to value (list of actor names).
    """
    return df.groupby('Film')['Actor'].apply(list).to_dict()

def _build_actor_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an actor-level dataframe with aggregated filmographies. Groups
    input df by actor, actor ID, aggregating titles for each actor into a
    list. The resulting df has one row per unique actor and a 'Film' column
    containing that actor's films.

    :param df: Movie data with Actor, ActorID, and Film columns.
    :return: Dataframe with columns ['Actor', 'ActorID', 'Film'] where
    'Film' is a list of film titles per actor.
    """
    return (df.groupby(['Actor', 'ActorID'])['Film']
            .apply(list).reset_index())

def _build_actors(actor_rows: pd.DataFrame, cast_dict: dict[str, list[str]]) \
        -> dict[str, Actor]:
    """
    Construct Actor domain objects and populate co-star relationships.
    Creates one Actor object per row in given actor_rows df and builds each
    actor's filmography and co-star set using the provided film-to-cast
    mapping.

    :param actor_rows: Dataframe with columns ['Actor', 'ActorID', 'Film'] where
    'Film' is a list of film titles per actor.
    :param cast_dict: Dict, key (film title) to value (list of actor names).
    :return: Dictionary mapping actor name to populated Actor objects.
    """
    # instantiate dict mapping actor name to actor objects.
    actors_dict: dict[str, Actor] = {}
    # helper func to create actor objects from actor data and store in dict
    actor_rows.apply(_process_actor_row, axis=1, args=(actors_dict,))
    # for each actor in the dictionary of actors
    for actor_obj in actors_dict.values():
        # for each film title in the current actor's filmography
        for film_title in actor_obj.films:
            # add the cast list to a set in the actor object (remove duplicates)
            actor_obj.costars.update(cast_dict[film_title])
        # remove the actor from their own costar list
        actor_obj.costars.remove(actor_obj.name)
    # return tuple containing dictionaries of actors, casts
    return actors_dict


class Loader:
    def __init__(self, fpath: str):
        """
          Loader for movie dataset and actor graph construction. This class
          handles loading movie data from CSV into dataframe, aggregating
          actor-level filmographies, building Actor objects and co-star
          relationships, and prompting user for two actor names for querying.
          Attributes:
              - filepath (Path): Path to the movie dataset CSV file.
              - actor_1 (str): The user-provided origin actor.
              - actor_2 (str): The user-provided destination actor.
              - actor_dict (Dict[str, Actor]): Dictionary mapping actor
              names to Actor objects.
          """
        self.filepath: Path = Path(fpath)
        self.actor_1: str
        self.actor_2: str
        self.actor_1, self.actor_2 = _get_user_input()
        self.actor_dict: dict[str, Actor] = self._load_data()

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Load the movie dataset from disk into a pandas Dataframe.
        :return: Dataframe containing the movie dataset.
        """
        return pd.read_csv(self.filepath, dtype=str)

    def _load_data(self) -> dict[str, Actor]:
        """
        Load movie data and construct the Actor graph. Reads the raw dataset
        from disk, derives actor-level filmographies and film-to-cast
        mappings, and builds populated Actor objects with co-star
        relationships.

        :return: Dictionary mapping actor name to Actor objects.
        """
        df = self._load_dataframe()
        actor_rows = _build_actor_rows(df)
        cast_dict = _build_cast_dict(df)
        return _build_actors(actor_rows, cast_dict)