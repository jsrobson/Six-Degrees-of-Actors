from dataLoader import get_input, load_data
from classes.actorQuery import ActorQuery

FILEPATH = "data/actorfilms.csv"

actors_dict = load_data(FILEPATH)
actors_in = get_input()

query = ActorQuery(actors_in[0], actors_in[1])
query.run_augmented_bfs(actors_dict)
query.print_string()