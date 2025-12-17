"""
Main script to compute the Bacon number between two actors.

Workflow:
1. Load movie data from a CSV using Loader.
2. Prompt the user for two actor names.
3. Build an Actor graph from the movie dataset.
4. Compute the shortest path (Bacon number) between the two actors using
   ActorQuery's BFS traversal.
5. Print the Bacon number and detailed path with shared films.

Modules:
- utils.loader: Handles CSV loading and Actor object construction.
- processor.actorQuery: Handles pathfinding and Bacon number computation.
"""

from utils.loader import Loader
from processor.actorQuery import ActorQuery

FILEPATH = "data/actorfilms.csv"

# Load dataset and prompt user for actors
loader = Loader(FILEPATH)

# Initialize ActorQuery with user-provided actors
query = ActorQuery(loader.actor_1, loader.actor_2)

# Compute the Bacon number path
query.run_bfs(loader.actor_dict)

# Print the path and the Bacon number
query.print_string()