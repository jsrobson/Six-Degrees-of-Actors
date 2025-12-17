# Six-Degrees-of-Actors ("Baconator")

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)

This program is an application of [Dijkstra's canonical shortest path algorithm (1956)](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) (Breadth-First-Search, BFS) using non-negative edge weights to find the number of steps distance between two actors (nodes) in a database given intersections (other actors) in their filmography (edges). This is a sector-specific application of the academic [Erdős number](https://en.wikipedia.org/wiki/Erdős_number).

The program accepts two input strings from a user – **origin actor and destination actor** – and applies the shortest path algorithm and an complementary path reconstruction algorithm to find both :
- The [Bacon Number](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon#Bacon_numbers) of the destination actor (the number of degrees of separation from the origin)
- The co-starring actors (and films in which they co-starred) in between the origin and destination.

This project was inspired by a long walk listening to Katie Goldin and Alex Schmidt discuss the history of Bacon Numbers on their podcast [Secretly Incredibly Fascinating](https://maximumfun.org/episodes/secretly-incredibly-fascinating/secretly-incredibly-fascinating-six-degrees-of-kevin-bacon) and the clear connection of graph theory to effectively model this concept.

---

## Data Attribution

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)  

The program uses a cleaned database of scraped IMDB data for 10k actors, made available under **Creative Commons licence CC0: Public Domain** by Kaggle user HugeQuiz.com.  

The original dataset can be found [here](https://www.kaggle.com/datasets/darinhawley/imdb-films-by-actor-for-10k-actors?select=actorfilms.csv).


---

## Features
- **CSV Input**: Load actor-film datasets from CSV files.  
- **Actor Graph Construction**: Build Actor objects with filmographies and co-star relationships.  
- **Bacon Number Calculation**: Compute shortest paths between two actors using BFS.  
- **Shared Filmography**: Display films connecting each pair of actors along the path.  
- **Console Interface**: CLI-driven interface to prompt user for origin and destination actors and print detailed paths.

---

## Installation
1. Clone the repository
```bash
git clone https://github.com/jsrobson/Six-Degrees-of-Actors.git
cd Six-Degrees-of-Actorss
```
2. Create a virtual environment (recommended)
```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage
```bash
python app.py
```
1. Enter the names of the **origin actor** and **destination actor** when prompted.
2. The program calculates the **Bacon number** and prints a path with shared films.

---

## Example Output
```bash
BACON NUMBER
Emily Blunt has a Bacon number of 2 from Harrison Ford.
1: Harrison Ford and Alan Arkin starred together in Firewall
2: Alan Arkin and Emily Blunt starred together in Sunshine Cleaning, The Muppets
```
Note that pathfinding is not deterministic. Running a query on the same actors multiple times may yield a different path, though the Bacon number will remain the same.

---

## Project Structure
```bash
Six-Degrees-of-Actors/
├── app.py                 # Entry point for user to run queries
├── data/                  # CSV dataset
├── models/                # Actor and Film domain objects
├── processor/             # ActorQuery logic – BFS / shortest-path
├── tests/                 # Unit tests for Actor, Film, ActorQuery, and Loader
├── utils/                 # Loader for CSV processing and Actor graph construction
├── requirements.txt       # Python dependencies used in program
```

---

## Dependencies
Key libraries are:
- **Pandas**: Data manipulation
- **Dataclasses**: For data-driven Actor and Film objects

This is echoed in **requirements.txt**.

---

## Testing
Run the unit tests:
```bash
pytest tests\
```
Tests include:
- Actor graph creation
- BFS pathfinding
- Shared film computation

---

## Learning
- **Graph traversal algorithms** – Implementing BFS and shortest path calculations on a dataset representing nodes, edges
- **Object-oriented design** – Actor and Film domain modeling
- **Data preprocessing and aggregation** – Handling CSV input and constructing co-star relationships
- **Project organization** – Clear separation of data loading, processing, program function, and testing for maintainable code

---

## Licence
[MIT Licence](https://choosealicense.com/licenses/mit/)
