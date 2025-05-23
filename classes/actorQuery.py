from math import inf
from queue import Queue

def generate_actors_path(start, end, prev):
    """
    Function generates a path from the starting actor to ending actor in chain.
    :param start: Originating actor, string
    :param end: Concluding actor, string
    :param prev: Dictionary containing previous path nodes
    :return: List of actors in path (start -> end)
    """
    # initialize empty path list and initialize ptr to end point
    path = []
    ptr = end
    # while the pointer has not reached the starting point (actor)
    while ptr != start:
        # append the pointer actor to the path
        path.append(ptr)
        # reset the pointer to the previous item in path
        ptr = prev.get(ptr)
        # if the ptr is none, we return an empty list
        if ptr is None:
            return []
    # at conclusion of loop, append the starting actor
    path.append(start)
    # reverse the list to go from start to end
    path.reverse()
    return path

def generate_complete_path(actors_dict: dict, path: list) -> dict:
    """
    Given a path of actors, function builds a shared filmography.
    :param actors_dict: Dictionary of actors (k: name, v: object)
    :param path: List of actors in path (start -> end)
    :return: dict, shared acting credit and filmography for each actor pair
    in path.
    """
    # initialize a dictionary to store the complete path (index,
    # tuple containing actor pair as string, and shared credits)
    c_path = dict()
    # use enumerate to get index and zip to get pairs in list
    for index, (curr_actor, next_actor) in enumerate(zip(path, path[1:])):
        # get the filmographies for actor pairs
        curr_act_films = actors_dict[curr_actor].films
        next_act_films = actors_dict[next_actor].films
        # store the actor name pair and the shared films in their filmography
        c_path[index] = ((curr_actor, next_actor), list(set(curr_act_films) &
                                                        set(next_act_films)))
    return c_path

class ActorQuery:
    def __init__(self, actor_1: str, actor_2: str):
        self.act_origin = actor_1
        self.act_destination = actor_2
        self.valid = False
        self.bacon_number = inf
        self.complete_path = dict()

    def print_string(self):
        """
        Method prints the path from the origin actor to the destination actor.
        :return: None
        """
        if not self.valid:
            print("One or both of search terms not found.")
            return
        print("\nBACON NUMBER")
        b_out = (f"{self.act_destination} has a Bacon number of "
                 f"{self.bacon_number} from {self.act_origin}.")
        print(b_out, "\n\nPATH")
        for key in sorted(self.complete_path.keys()):
            record = self.complete_path[key]
            act_1 = record[0][0]
            act_2 = record[0][1]
            join_str = ", ".join(record[1])
            p_out = (f"{key + 1}: {act_1} and {act_2} starred together in"
                     f" {join_str}")
            print(p_out)


    # assume dictionary containing k: actor name, v: actor objects
    def run_augmented_bfs(self, actors_dict: dict) -> None:
        # get the origin key (analogous to s in Roughgarden)
        origin_key, destination_key = self.act_origin, self.act_destination

        if origin_key in actors_dict and destination_key in actors_dict:
            self.valid = True
        else:
            return
        # mark origin as explored, all other vertices as unexplored
        actors_dict[origin_key].explored = True
        # distance from self is 0
        actors_dict[origin_key].bacon_number = 0
        # check not self
        if self.act_origin == self.act_destination:
            self.bacon_number = 0
            print("Origin is same as destination")
            return
        # initialize queue data structure, with origin as initial entry
        q = Queue()
        q.put(actors_dict[origin_key])
        # dict to store previous path nodes
        prev = {}
        # while queue is not empty do
        while not q.empty():
            # remove vertex from front of queue, call it v
            subj_actor = q.get()
            b_number = subj_actor.bacon_number
            # for each edge (film) (v, w) in v's adjacency list, do
            # note: pre-processed costars, so can go directly to this data
            costars = subj_actor.costars
            for costar in costars:
                # if costar is unexplored, then
                if not actors_dict[costar].explored:
                    # mark costar as explored
                    actors_dict[costar].explored = True
                    #l(costar) = l(actor) + 1
                    actors_dict[costar].bacon_number = b_number + 1
                    # add costar to end of queue
                    q.put(actors_dict[costar])
                    # store prev path
                    prev[actors_dict[costar].name] = subj_actor.name
        # update paired bacon number
        self.bacon_number = actors_dict[self.act_destination].bacon_number
        # generate simple actors path and use it to build a complete path
        actors_path = generate_actors_path(origin_key, destination_key, prev)
        self.complete_path = generate_complete_path(actors_dict, actors_path)
