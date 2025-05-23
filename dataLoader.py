import pandas as pd
from classes.actor import Actor

def get_input() -> tuple[str, ...]:
    """
    Helper function gets user input from command line prompt.
    :return: Tuple of stored user input
    """
    # initialize list to store input
    actors = list()
    print("USER INPUT")
    # for each pairing
    for order in ["first", "second"]:
        # get user input given prompt
        user_in = input(f"Please type the name of the {order} actor: ")
        # convert user input to string and append to input store
        actors.append(str(user_in))
    # return tuple converted from list
    return tuple(actors)

def process_actor_row(row: pd.Series, a_dict: dict):
    """
    Given a row of data, function builds an actor object from row fields
    :param row: Pandas row information for actors, movies
    :param a_dict: Dictionary of actors (k: name, v: object)
    :return: nothing, dictionary updated.
    """
    # pull actor name, id, films from row
    act_name = row['Actor']
    act_id = row['ActorID']
    films = row['Film']
    # build actor object from data and set to actor name as key
    a_dict[act_name] = Actor(act_name, act_id, films)

def load_data(filepath: str) -> dict:
    # read in csv data as dataframe
    df = pd.read_csv(filepath, dtype=str)
    # build dictionary to hold k: string, v: objects for actors
    actors_dict = dict()
    # create the cast list for each film and store as dict (k: title, v: list)
    cast_dict = df.groupby('Film')['Actor'].apply(list).to_dict()
    # from df, group data by actor name
    actors_df = df.groupby(['Actor', 'ActorID'])['Film'].apply(
        list).reset_index()
    # helper func to create actor objects from actor data and store in dict
    actors_df.apply(process_actor_row, axis=1, args=(actors_dict,))
    # for each actor in the dictionary of actors
    for actor_obj in actors_dict.values():
        # for each film title in the current actor's filmography
        for film_title in actor_obj.films:
            # pull the cast list from the corresponding film cast dictionary
            cast_list = cast_dict[film_title]
            # add the cast list to a set in the actor object (remove duplicates)
            actor_obj.costars.update(cast_list)
        # remove the actor from their own costar list
        actor_obj.costars.remove(actor_obj.name)
    # return tuple containing dictionaries of actors, casts
    return actors_dict